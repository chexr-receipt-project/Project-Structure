from logging import info
from typing import Optional

from odmantic import AIOEngine
from pymongo import ASCENDING

from .schema import BankTransaction


async def initialize_schema(database: AIOEngine):
    info("Initializing Bank Repository")

    collection = database.get_collection(BankTransaction)
    await collection.create_index([
        (+BankTransaction.bank_id, ASCENDING),
        (+BankTransaction.transaction_id, ASCENDING)
    ], name="transaction_bank_id", unique=True)


async def get_bank_transaction(database: AIOEngine, bank_id: str, transaction_id: str) -> Optional[
                                   BankTransaction]:
    return await database.find_one(BankTransaction,
                                   (BankTransaction.transaction_id == transaction_id) &
                                   (BankTransaction.bank_id == bank_id)
                                   )


async def insert_bank_transaction(database: AIOEngine, bank_id: str, transaction: BankTransaction) -> \
        Optional[BankTransaction]:
    if transaction.id is not None:
        raise ValueError("id must be empty")
    transaction.bank_id = bank_id
    return await database.save(transaction)
