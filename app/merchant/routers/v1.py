from fastapi import APIRouter, Depends
from ..schema import Transaction
from ...core.database import get_database
from ..model.merchant_repository import get_merchant_transaction, insert_merchant_transaction

## FIXME will be recovered by authentication
MERCHANT_ID = "MERCHANTID"

merchant_v1 = APIRouter(
    prefix="/merchant/v1",
    tags=["merchant", "v1"],
    responses={404: {"description": "Not Found"}}
)


# based on https://developers.tryflux.com/#operation/MerchantPost
@merchant_v1.put("/transaction")
async def new_transaction(transaction: Transaction, database=Depends(get_database)):
    """ Add a new transaction from the merchant"""
    saved_transaction = await get_merchant_transaction(database, MERCHANT_ID, transaction.id)

    if saved_transaction:
        raise Exception("Transaction already exists")

    await insert_merchant_transaction(database, MERCHANT_ID, transaction)


