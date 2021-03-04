from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from ..schema import Transaction
from ...core.database import get_database
from ...core.utils import CHEXR_ENCODER
from ..model.merchant_repository import get_merchant_transaction, insert_merchant_transaction
from simplejson import dump

## FIXME will be recovered by authentication
MERCHANT_ID = "MERCHANTID"

merchant_v1 = APIRouter(
    prefix="/merchant/v1",
    tags=["merchant", "v1"],
    responses={404: {"description": "Not Found"}}
)


# based on https://developers.tryflux.com/#operation/MerchantPost
@merchant_v1.put("/transaction", response_model=Transaction)
async def new_transaction(transaction: Transaction, database=Depends(get_database)):
    """ Add a new transaction from the merchant"""
    saved_transaction = await get_merchant_transaction(database, MERCHANT_ID, transaction.transaction_id)

    if saved_transaction:
        raise Exception("Transaction already exists")

    saved_transaction = await insert_merchant_transaction(database, MERCHANT_ID, transaction)

    return jsonable_encoder(saved_transaction, custom_encoder=CHEXR_ENCODER)



