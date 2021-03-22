from logging import info, error, debug
import re
from typing import Callable
from asyncio import run

from bson import ObjectId
from odmantic import AIOEngine
from pymongo.errors import DuplicateKeyError

from chexr.core.database import get_database, startup_db
from chexr.matching.matching_repository import register_match
from chexr.merchant.merchant_repository import search_merchant_transaction_by_auth_code, get_merchant_transaction
from chexr.bank.bank_repository import search_payment_by_auth_code, get_bank_transaction
from chexr.matching.schema import Matching

__PATTERN_MERCHANT_TRANSACTION = "^transaction_id:(.+)"
__PATTERN_BANK_TRANSACTION = "^bank_transaction_id:(.+)"
__DATABASE_STARTED = False


async def matching_queue_handler(event, _):
    if not __DATABASE_STARTED:
        await startup_db()

    records = event['Records']
    info(f"Processing {len(records)} messages on matching queue")

    for record in records:
        body_ = record['body']
        if await evaluate_and_call_if_match(__PATTERN_MERCHANT_TRANSACTION, body_, process_merchant_transaction):
            debug("Processed merchant transaction '%s'", body_)
            continue
        if await evaluate_and_call_if_match(__PATTERN_BANK_TRANSACTION, body_, process_bank_transaction):
            debug("Processed bank transaction '%s'", body_)
            continue
        error(f"Message '%s' is not understandable and will be ignored", body_)


async def evaluate_and_call_if_match(pattern: str, value: str, function_to_call_if_match: Callable):
    result = re.search(pattern, value)
    if result:
        await function_to_call_if_match(result.group(1))
        return True
    return False


async def process_merchant_transaction(transaction_id: str):
    debug("Processing merchant transaction id %s", transaction_id)

    database = get_database()
    transaction = await get_merchant_transaction(database, transaction_id=ObjectId(transaction_id))

    if transaction is None:
        raise Exception(f"Transaction {transaction_id} not found")

    debug("Found transaction, searching for payments")
    for payment in transaction.payments:
        if payment.card:
            auth_code = payment.card.auth_code
            debug("Searching payment auth %s", auth_code)
            bank_transaction = await search_payment_by_auth_code(database, auth_code)
            if bank_transaction is not None:
                debug("Found payment auth %s, creating matching document", auth_code)
                await _match_transactions(database, transaction.merchant_id, transaction.transaction_id,
                                    bank_transaction.bank_id, bank_transaction.transaction_id)
            else:
                info("Merchant transaction id %s has a payment auth code %s not found in database. Bank should send it"
                     " later", transaction_id, auth_code)


async def process_bank_transaction(bank_transaction_id: str):
    debug("Processing bank transaction id %s", bank_transaction_id)

    database = get_database()
    bank_transaction = await get_bank_transaction(database, transaction_id=ObjectId(bank_transaction_id))

    if bank_transaction is None:
        raise Exception(f"Bank Transaction {bank_transaction_id} not found")

    if not bank_transaction.card:
        debug(f"Bank transaction {bank_transaction_id} is not a card transaction and will be ignored for matching "
              f"purposes")
        return

    debug("Found bank transaction, searching for merchant transaction")

    merchant_transaction = await search_merchant_transaction_by_auth_code(database, bank_transaction.card.auth_code)

    if not merchant_transaction:
        info("Bank transaction %s has a payment auth code %s without a merchant transaction. Merchant should send it "
             "later", bank_transaction_id, bank_transaction.card.auth_code)
        return

    debug("Found merchant transaction %s, creating matching document", merchant_transaction.id)
    await _match_transactions(database, merchant_transaction.merchant_id, merchant_transaction.transaction_id,
                              bank_transaction.bank_id, bank_transaction.transaction_id)


async def _match_transactions(database: AIOEngine, merchant_id: str, merchant_transaction_id: str, bank_id: str,
                              bank_transaction_id: str):
    new_matching = Matching(
        merchant_id=merchant_id,
        merchant_transaction_id=merchant_transaction_id,
        bank_transaction_id=bank_transaction_id,
        bank_id=bank_id
    )

    try:
        await register_match(database, new_matching)
    except DuplicateKeyError:
        debug("Matching already registered, ignoring")
