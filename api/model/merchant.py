from pydantic import BaseModel
from enum import Enum
from datetime import datetime
from decimal import Decimal
from typing import List, Optional


class TransactionPaymentType(Enum):
    CARD = "CARD"
    CASH = "CASH"
    CHECQUE = "CHECQUE"
    GIFTCARD = "GIFTCARD"
    OTHER = "OTHER"


class TransactionPaymentCardDetails(BaseModel):
    bin: str
    last_four: str
    auth_code: str
    scheme: str


class TransactionPayment(BaseModel):
    type: TransactionPaymentType
    method: str
    amount: Decimal
    timestamp: Optional[datetime]
    card: Optional[TransactionPaymentCardDetails]


class TransactionItem(BaseModel):
    sku: str
    description: str
    category: str
    quantity: Decimal
    price: Decimal
    tax: Decimal


class TransactionStatus(Enum):
    """Transaction status"""
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


class Transaction(BaseModel):
    id: str
    merchant_id: str
    transaction_date: datetime = datetime.now()
    amount: Decimal
    currency: str
    tax: Decimal
    items: List[TransactionItem]
    payments: List[TransactionPayment]
    status: TransactionStatus = TransactionStatus.COMPLETED




