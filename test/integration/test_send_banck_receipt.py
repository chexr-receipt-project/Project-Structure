from odmantic import AIOEngine

from chexr.bank.schema import Bank, BankTransaction
from chexr.core.database import get_database, startup_db
from chexr.matching.schema import Matching
from chexr.merchant.schema import Transaction, TransactionItem, TransactionPayment, TransactionPaymentType, \
    TransactionPaymentCardDetails
from function_matching.main import matching_queue_handler
import asyncio


async def test_send_bank_receipt():
    await startup_db()

    database = get_database();

    # clear collections
    await empty_collection(database, Bank)
    await empty_collection(database, Transaction)
    await empty_collection(database, BankTransaction)
    await empty_collection(database, Matching)

    # store bank
    bank = await database.save(Bank(url_upload_receipts="http://localhost:8888", jws_signature="AAA", bank_name="dummy bank"))
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

    # store match

    # start function


async def empty_collection(database: AIOEngine, model):
    for doc in await database.find(model):
        await database.delete(doc)


if __name__ == '__main__':
    asyncio.run(test_send_bank_receipt())
