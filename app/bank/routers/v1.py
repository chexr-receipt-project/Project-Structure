from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder


from ...core.database import get_database
from ...core.utils import CHEXR_ENCODER
from ...core.queue import send_message
from ...core.config import settings

## FIXME will be recovered by authentication
BANK_ID = "BANKID"

bank_v1 = APIRouter(
    prefix="/bank/v1",
    tags=["bank", "v1"],
    responses={404: {"description": "Not Found"}}
)


# based on https://developers.tryflux.com/#operation/MerchantPost
@bank_v1.put("/transaction", response_model=Transaction)
async def new_transaction(transaction: Transaction, database=Depends(get_database)):
    """ Add a new transaction from the merchant"""
    saved_transaction = await get_merchant_transaction(database, MERCHANT_ID, transaction.transaction_id)

    if saved_transaction:
        raise Exception("Transaction already exists")

    saved_transaction = await insert_merchant_transaction(database, MERCHANT_ID, transaction)

    send_message(settings.MATCHING_QUEUE_URL, f'transaction_id:{saved_transaction.id}')

    return saved_transaction



