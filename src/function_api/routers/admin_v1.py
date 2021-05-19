from typing import List

from fastapi import APIRouter, Depends

from chexr.bank.bank_repository import merge_bank, list_banks
from chexr.bank.schema import Bank
from chexr.core.database import get_database
from chexr.merchant.merchant_repository import merge_merchant, list_merchants
from chexr.merchant.schema import Merchant
from chexr.matching.schema import Matching
from chexr.matching.matching_repository import list_matchings
from ..utils import verify_admin

admin_v1 = APIRouter(
    prefix="/admin/v1",
    tags=["admin", "v1"],
    responses={404: {"description": "Not Found"}},
    dependencies=[Depends(verify_admin)])


@admin_v1.put("/bank", response_model=Bank, description="Insert or update (if id is already registered) a bank")
async def new_bank(bank: Bank, database=Depends(get_database)):
    return await merge_bank(database, bank)


@admin_v1.get("/bank", response_model=List[Bank], description="List banks")
async def list_bank(database=Depends(get_database)):
    return await list_banks(database)


@admin_v1.put("/merchant", response_model=Merchant, description="Insert or update (if id is already registered) a merchant")
async def new_bank(merchant: Merchant, database=Depends(get_database)):
    return await merge_merchant(database, merchant)


@admin_v1.get("/merchant", response_model=List[Merchant], description="List merchants")
async def list_merchant(database=Depends(get_database)):
    return await list_merchants(database)


@admin_v1.get("/matching", response_model=List[Matching], description="List all sent or unsent matchings")
async def list_matching(list_sent=False, database=Depends(get_database)):
    return await list_matchings(list_sent, database)
