from typing import Optional
from ..schema import Transaction
from odmantic import AIOEngine
from logging import info
from pymongo import ASCENDING


async def initialize_schema(database: AIOEngine):
    info("Initializing Merchant Repository")

    collection = database.get_collection(Transaction)
    await collection.create_index([
        (+Transaction.merchant_id, ASCENDING),
        (+Transaction.transaction_id, ASCENDING)
    ], name="transaction_merchant_id", unique=True)


async def get_merchant_transaction(database: AIOEngine, merchant_id: str, transaction_id: str) -> Optional[
                                   Transaction]:
    return await database.find_one(Transaction,
                                   (Transaction.transaction_id == transaction_id) &
                                   (Transaction.merchant_id == merchant_id)
                                   )


async def insert_merchant_transaction(database: AIOEngine, merchant_id: str, transaction: Transaction) -> \
        Optional[Transaction]:
    if transaction.id is not None:
        raise ValueError("id must be empty")
    transaction.merchant_id = merchant_id
    return await database.save(transaction)
