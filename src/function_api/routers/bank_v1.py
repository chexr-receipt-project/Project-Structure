from fastapi import APIRouter, Depends

from chexr.bank.bank_repository import insert_bank_transaction
from chexr.bank.schema import BankTransaction
from chexr.core.config import settings
from chexr.core.database import get_database
from chexr.core.queue import send_message

## FIXME will be recovered by authentication
BANK_ID = "BANKID"

bank_v1 = APIRouter(
    prefix="/bank/v1",
    tags=["bank", "v1"],
    responses={404: {"description": "Not Found"}}
)


# based on https://developers.tryflux.com/#operation/MerchantPost
@bank_v1.put("/transaction", response_model=BankTransaction)
async def new_transaction(transaction: BankTransaction, database=Depends(get_database)):
    """ Add a new transaction from the merchant"""
    saved_transaction = await insert_bank_transaction(database, BANK_ID, transaction)

    send_message(settings.MATCHING_QUEUE_URL, f'bank_transaction_id:{saved_transaction.id}')

    return saved_transaction



