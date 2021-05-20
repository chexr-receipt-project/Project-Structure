from logging import info
from typing import Iterable

from odmantic import AIOEngine
from pymongo import ASCENDING

from .schema import Matching
from ..bank.schema import Bank


async def initialize_schema(database: AIOEngine):
    info("Initializing Matching Repository")

    collection = database.get_collection(Matching)
    await collection.create_index([
        (+Matching.bank_id, ASCENDING),
        (+Matching.sent_to_bank, ASCENDING),
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


async def search_unsent_matching_by_bank(database: AIOEngine, bank: Bank) -> Iterable[Matching]:
    return await database.find(Matching, (Matching.bank_id == bank.id) & (Matching.sent_to_bank == False))


async def mark_matching_as_sent(database: AIOEngine, matching: Matching):
    matching.sent_to_bank = True
    await database.save(matching)


async def list_matchings(list_sent: bool, database: AIOEngine):
    return await database.find(Matching, Matching.sent_to_bank == list_sent)
