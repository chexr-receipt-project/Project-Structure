from datetime import datetime

from bson import ObjectId
from odmantic import Model, Field


class Matching(Model):
    merchant_id: str
    merchant_transaction_id: str
    bank_transaction_id: str
    bank_id: str
    matching_date: datetime = Field(default_factory=datetime.utcnow)
    sent_to_bank: str = False

    def __str__(self):
        return f"matching({self.bank_id},{self.bank_transaction_id},{self.merchant_id},{self.merchant_transaction_id})"

