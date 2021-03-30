from datetime import datetime

import aiohttp
from odmantic import AIOEngine

from chexr.bank.schema import Bank, BankTransaction, Card
from chexr.core.database import get_database, startup_db
from chexr.matching.schema import Matching
from chexr.merchant.schema import Transaction, TransactionItem, TransactionPayment, TransactionPaymentType, \
    TransactionPaymentCardDetails
import asyncio
from aioresponses import aioresponses

from function_send_bank_receipt.main import send_bank_receipt


async def test_send_bank_receipt():
    await startup_db()

    database = get_database();

    # clear collections
    await empty_collection(database, Bank)
    await empty_collection(database, Transaction)
    await empty_collection(database, BankTransaction)
    await empty_collection(database, Matching)

    # store bank
    url_upload = "http://127.0.0.1:8888/"
    bank = await database.save(
        Bank(url_upload_receipts=url_upload, jws_signature="AAA", bank_name="dummy bank"))
    # store merchant receipt
    transaction = Transaction(transaction_id="T1", merchant_id="M1", store_id="S1", amount=10, currency="BRL",
                              items=[TransactionItem(sku="SKU1", description="Item", category="Category", quantity=1,
                                                     price=10, tax=1)
                                     ],
                              payments=[TransactionPayment(type=TransactionPaymentType.CARD, method="pin", amount=10,
                                                           card=TransactionPaymentCardDetails(bin="123456",
                                                                                              last_four="1234",
                                                                                              auth_code="XXYYZZ",
                                                                                              scheme="MASTERCARD"))
                                        ]
                              )
    await database.save(transaction)
    # store bank receipt
    bank_transaction = BankTransaction(transaction_id="BTID1", bank_id=str(bank.id), customer_id="C1", amount=10,
                                       transaction_date=datetime(2021, 1, 11, 11, 00),
                                       card=Card(bin="123456",
                                                 last_four="1234",
                                                 auth_code="XXYYZZ",
                                                 scheme="MASTERCARD")
                                       )
    await database.save(bank_transaction)
    # store match
    matching = await database.save(
        Matching(merchant_id=transaction.merchant_id, merchant_transaction_id=transaction.transaction_id,
                 bank_transaction_id=bank_transaction.transaction_id, bank_id=bank_transaction.bank_id)
    )

    # mock server reply
    with aioresponses() as m:
        m.put(url_upload)
        await send_bank_receipt(None, None)


async def empty_collection(database: AIOEngine, model):
    for doc in await database.find(model):
        await database.delete(doc)


if __name__ == '__main__':
    asyncio.run(test_send_bank_receipt())
