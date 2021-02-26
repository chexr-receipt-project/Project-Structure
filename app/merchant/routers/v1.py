from fastapi import APIRouter
from ..schema import Transaction

merchant_v1 = APIRouter(
    prefix="/merchant/v1",
    tags=["merchant","v1"],
    responses={404: {"description":"Not Found"}}
)


# based on https://developers.tryflux.com/#operation/MerchantPost
@merchant_v1.put("/transaction")
async def new_transaction(transaction: Transaction):
    """ Add a new transaction from the merchant"""
    pass
