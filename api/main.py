from fastapi import FastAPI
from model.merchant import Transaction
from mangum import Mangum
import uvicorn

app = FastAPI(title="Cherx API")


@app.get("/")
async def root():
    return {"message": "Chexr Receipts"}


@app.get("/hello")
async def hello():
    return {"message": "Hello World"}


# based on https://developers.tryflux.com/#operation/MerchantPost
@app.put("/merchant/transaction")
async def new_transaction(transaction: Transaction):
    """ Add a new transaction from the merchant"""
    pass


handler = Mangum(app=app)

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)