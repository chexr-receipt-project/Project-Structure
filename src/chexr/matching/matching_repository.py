from logging import info

from odmantic import AIOEngine
from pymongo import ASCENDING

from .schema import Matching


async def initialize_schema(database: AIOEngine):
    info("Initializing Matching Repository")

    collection = database.get_collection(Matching)
    await collection.create_index([
        (+Matching.sent_to_bank, ASCENDING),
        (+Matching.bank_id, ASCENDING),
        (+Matching.matching_date, ASCENDING)
    ], name="matching_send_to_bank")

    await collection.create_index([
        (+Matching.bank_id, ASCENDING),
        (+Matching.bank_transaction_id, ASCENDING),
        (+Matching.merchant_id, ASCENDING),
        (+Matching.merchant_transaction_id, ASCENDING)],
        name="matching_unique", unique=True)


async def register_match(database: AIOEngine, matching: Matching):
    await database.save(matching)
