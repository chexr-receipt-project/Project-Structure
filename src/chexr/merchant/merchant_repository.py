from typing import Optional, Tuple

from bson import ObjectId

from .schema import Transaction
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

    await collection.create_index("payments.card.auth_code", name="transaction_merchant_auth_code", sparse=True)


async def get_merchant_transaction(database: AIOEngine, transaction_id: ObjectId = None,
                                   merchant_transaction: Tuple[str,str] = None) -> Optional[
                                   Transaction]:

    if id is not None:
        return await database.find_one(Transaction, Transaction.id == transaction_id)

    return await database.find_one(Transaction,
                                   (Transaction.transaction_id == merchant_transaction[0]) &
                                   (Transaction.merchant_id == merchant_transaction[1])
                                   )


async def search_merchant_transaction_by_auth_code(database: AIOEngine, auth_code: str) -> Optional[Transaction]:

    return await database.find_one(Transaction, {"payments.card.auth_code": auth_code})


async def insert_merchant_transaction(database: AIOEngine, merchant_id: str, transaction: Transaction) -> \
        Optional[Transaction]:
    if transaction.id is not None:
        raise ValueError("id must be empty")
    transaction.merchant_id = merchant_id
    return await database.save(transaction)
