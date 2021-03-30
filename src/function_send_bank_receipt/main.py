from logging import info, error

import aiohttp
from odmantic import AIOEngine

from chexr.bank.bank_repository import list_banks
from chexr.bank.schema import Bank, BankReceipt
from chexr.core.database import get_database, startup_db
from chexr.matching.matching_repository import search_unsent_matching_by_bank, mark_matching_as_sent
from chexr.matching.schema import Matching
from chexr.merchant.merchant_repository import get_merchant_transaction

__DATABASE_STARTED = False


async def send_bank_receipt(_, __):
    if not __DATABASE_STARTED:
        await startup_db()

    info("Starting function to send receipts to banks")

    database = get_database()

    for bank in await list_banks(database):
        await process_receipts_to_bank(database, bank)

    info("Finished function to send receipts")


async def process_receipts_to_bank(database: AIOEngine, bank: Bank):
    info("Processing receipts to bank %s", bank.bank_name)
    for matching in await search_unsent_matching_by_bank(database, bank):
        await process_matching(database, bank, matching)
    info("Finished processing bank %s", bank.bank_name)


async def process_matching(database: AIOEngine, bank: Bank, matching: Matching):
    try:
        info("Processing %s", matching)
        merchant_transaction = await get_merchant_transaction(database,
                                                              merchant_transaction=(matching.merchant_id,
                                                                                    matching.merchant_transaction_id))

        receipt = BankReceipt(
            bank_transaction_id=matching.bank_transaction_id,
            merchant_transaction_id=matching.merchant_transaction_id,
            amount=merchant_transaction.amount,
            currency=merchant_transaction.currency,
            transaction_date=merchant_transaction.transaction_date,
            tax=merchant_transaction.tax,
            payments=merchant_transaction.payments,
            items=merchant_transaction.items
        )

        await send_receipt_to_bank(bank, receipt)

        await mark_matching_as_sent(database, matching)

        info("Matching processed %s", matching)
    except Exception as e:
        error("Matching %s got an error: %s", matching, e)


async def send_receipt_to_bank(bank: Bank, receipt: BankReceipt):
    # TODO actually, we need to sign the body and pass in this header the signature More in
    #  https://openbankinguk.github.io/read-write-api-site3/v3.1.4/profiles/read-write-data-api-profile.html#message-signing-2
    headers = {
        "x-jws-signature": bank.jws_signature,
        "CONTENT-TYPE": "application/json"
    }
    async with aiohttp.ClientSession() as session:
        body = receipt.json()
        async with session.request("PUT", bank.url_upload_receipts, data=body, headers=headers) as response:
            if response.status != 200:
                raise Exception(f"Bank url {bank.url_upload_receipts} send {response.status} when sending the receipt. "
                                f"Body: {response.content} ")
