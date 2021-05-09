from typing import Optional, Tuple

from bson import ObjectId

from .schema import Transaction, Merchant
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

    merchant_collection = database.get_collection(Merchant)
    await merchant_collection.create_index(
        [(+Merchant.client_id, ASCENDING)],
        name="merchant_client_id",
        unique=True
    )


async def get_merchant_transaction(database: AIOEngine, transaction_id: ObjectId = None,
                                   merchant_transaction: Tuple[str,str] = None) -> Optional[
                                   Transaction]:

    if transaction_id is not None:
        return await database.find_one(Transaction, Transaction.id == transaction_id)

    return await database.find_one(Transaction,
                                   (Transaction.merchant_id == merchant_transaction[0]) &
                                   (Transaction.transaction_id == merchant_transaction[1])
                                   )


async def search_merchant_transaction_by_auth_code(database: AIOEngine, auth_code: str) -> Optional[Transaction]:

    return await database.find_one(Transaction, {"payments.card.auth_code": auth_code})


async def insert_merchant_transaction(database: AIOEngine, merchant_id: str, transaction: Transaction) -> \
        Optional[Transaction]:
    if transaction.id is not None:
        saved_transaction = await database.find_one(Transaction, Transaction.id == transaction.id)
        if saved_transaction is not None:
            raise ValueError("Trying to insert an already defined merchant transaction id %s. Use update instead",
                             transaction.id)
    transaction.merchant_id = merchant_id
    return await database.save(transaction)


async def merge_merchant(database: AIOEngine, merchant: Merchant):
    return await database.save(merchant)


async def list_merchants(database: AIOEngine):
    return await database.find(Merchant)


async def find_merchant_by_client_id(database: AIOEngine, client_id: str):
    return await database.find_one(Merchant, Merchant.client_id == client_id)
