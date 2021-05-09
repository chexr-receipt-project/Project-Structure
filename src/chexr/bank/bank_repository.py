from logging import info
from typing import Optional, Tuple

from bson import ObjectId
from odmantic import AIOEngine
from pymongo import ASCENDING

from .schema import BankTransaction, Bank


async def initialize_schema(database: AIOEngine):
    info("Initializing Bank Repository")

    collection = database.get_collection(BankTransaction)
    await collection.create_index([
        (+BankTransaction.bank_id, ASCENDING),
        (+BankTransaction.transaction_id, ASCENDING)
    ], name="transaction_bank_id", unique=True)

    await collection.create_index([(+BankTransaction.card.auth_code, ASCENDING)], name="transaction_bank_auth_code",
                                  sparse=True)

    bank_collection = database.get_collection(Bank)
    await bank_collection.create_index(
        [(+Bank.client_id, ASCENDING)],
        name="bank_client_id",
        unique=True
    )


async def get_bank_transaction(database: AIOEngine, transaction_id: ObjectId = None,
                               bank_transaction: Tuple[str, str] = None) -> Optional[BankTransaction]:
    if id is not None:
        return await database.find_one(BankTransaction, BankTransaction.id == transaction_id)

    return await database.find_one(BankTransaction,
                                   (BankTransaction.transaction_id == bank_transaction[0]) &
                                   (BankTransaction.bank_id == bank_transaction[1])
                                   )


async def insert_bank_transaction(database: AIOEngine, bank_id: ObjectId, transaction: BankTransaction) -> \
        Optional[BankTransaction]:

    if transaction.id is not None:
        saved_transaction = await database.find_one(BankTransaction, BankTransaction.id == transaction.id)
        if saved_transaction is not None:
            raise ValueError("Trying to insert an already defined bank transaction id %s. Use update instead",
                             transaction.id)

    transaction.bank_id = bank_id
    return await database.save(transaction)


async def search_payment_by_auth_code(database: AIOEngine, auth_code: str):
    return await database.find_one(BankTransaction, (BankTransaction.card.auth_code == auth_code))


async def merge_bank(database: AIOEngine, bank: Bank):
    return await database.save(bank)


async def list_banks(database: AIOEngine):
    return await database.find(Bank)


async def find_bank_by_client_id(database: AIOEngine, client_id: str):
    return await database.find_one(Bank, Bank.client_id == client_id)
