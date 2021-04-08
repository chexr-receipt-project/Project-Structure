from fastapi import APIRouter

from chexr.bank.schema import BankReceipt

dummy_v1 = APIRouter(
    prefix="/dummy_bank/v1",
    tags=[],
    responses={404: {"description": "Not Found"}}
)


@dummy_v1.put("/receipt")
async def new_receipt(receipt: BankReceipt):
    print("Received a receipt")
    print(receipt)