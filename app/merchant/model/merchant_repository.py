from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import Optional
from ..schema import Transaction

MERCHANT_TRANSACTIONS_COLLECTION = 'merchant_transactions'


async def get_merchant_transaction(database: AsyncIOMotorDatabase, merchant_id: str, transaction_id: str) -> Optional[
                                   Transaction]:
    collection = database[MERCHANT_TRANSACTIONS_COLLECTION]
    return await collection.find_one({'merchant_id': merchant_id, 'transaction_id': transaction_id})


async def insert_merchant_transaction(database: AsyncIOMotorDatabase, merchant_id: str, transaction: Transaction) -> Optional[
                                   Transaction]:
    collection = database[MERCHANT_TRANSACTIONS_COLLECTION]
    # FIXME clone
    transaction.merchant_id = merchant_id

    await collection.insert(transaction)
