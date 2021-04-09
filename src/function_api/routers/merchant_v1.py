from fastapi import APIRouter, Depends

from chexr.core.config import settings
from chexr.core.database import get_database
from chexr.core.queue import send_message
from chexr.merchant.merchant_repository import insert_merchant_transaction
from chexr.merchant.schema import Transaction

from logging import debug, info

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
    print("Saving new transaction")
    saved_transaction = await insert_merchant_transaction(database, MERCHANT_ID, transaction)
    print("Transaction saved. Sending matching message")
    send_message(settings.MATCHING_QUEUE_URL, f'transaction_id:{saved_transaction.id}')
    print("Message sent, returning saved transaction")
    return saved_transaction
