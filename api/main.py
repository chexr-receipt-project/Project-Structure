from fastapi import FastAPI
from model.merchant import Transaction
app = FastAPI()


@app.get("/")
async def root():
    return {"message":"Chexr Receiptss"}


# based on https://developers.tryflux.com/#operation/MerchantPost
@app.put("/merchant/transaction")
async def new_transaction(transaction: Transaction):
    """ Add a new transaction from the merchant"""
    pass
