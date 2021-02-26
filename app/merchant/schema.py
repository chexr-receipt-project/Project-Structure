from pydantic import BaseModel, Field
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
    bin: Optional[str] = Field(description="The BIN/INN of the card. This is the usually the first 6 digits of the "
                                           "payment card.", regex="^d{4,8}")
    last_four: Optional[str] = Field(description="Last 4 digits of the payment card", regex="^d(4)")
    auth_code: str = Field(description="The authorization code used to match the payment with the bank clearing "
                                       "process")
    scheme: str = Field(description="The scheme of this card. For example: MASTERCARD, VISA, AMEX, etc")


class TransactionPayment(BaseModel):
    type: TransactionPaymentType
    method: str = Field(description="Method used to process this payment like `Contactless`, `Pin` etc")
    amount: Decimal = Field(description="The amount paid in this payment method")
    timestamp: Optional[datetime] = Field(description="The full date time (RFC3339), at second resolution or better. "
                                                      "This is for this particular payment and should be the "
                                                      "transaction authorization date if possible, or a timestamp "
                                                      "that is consistently offset from that (ie always 3 seconds "
                                                      "after authorization, vs a time that varies per transaction).")
    card: Optional[TransactionPaymentCardDetails] = Field(description="This field is mandatory in card payments")


class TransactionItem(BaseModel):
    sku: str = Field(..., description="`Stock Keeping Unit` that uniquely identify the item on merchant database", min_length=1)
    description: str = Field(..., description="Human friendly description", min_length=1)
    category: str
    quantity: Decimal = Field(description="Quantity purchases. It can be in fractions. Use the field `unity` if you "
                                          "want to append a unity")
    unity: str = Field(description="The unity that should be appended to the quantity. Eg `kg`", min_length=1)
    price: Decimal = Field(description="The amount of a single unit of the item, including all taxes")
    tax: Decimal = Field(description="The tax of a single unit")
    # There are a lot more attributes to add


class TransactionStatus(Enum):
    """Transaction status"""
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


class GeographicPoint(BaseModel):
    latitude: Decimal = Field(..., description="latitude of the location in decimal degrees using the WGS84 Geodetic "
                                             "system.")
    longitude: Decimal = Field(..., description="Longitude of the location in decimal degrees using the WGS84 Geodetic "
                                              "system.")


class Address(GeographicPoint):
    street_address: Optional[str]
    locality: Optional[str]
    region: Optional[str]
    postal_code: Optional[str]
    country: Optional[str]
    sovereign: Optional[str]


class Transaction(BaseModel):
    id: str = Field(..., description="Merchant unique transaction id", min_length=1)
    store_id: str = Field(..., description="Store unique identifier. Use a unique identifier if it is a single store "
                                           "merchant", min_length=1)
    terminal_id: Optional[str] = Field(description="Optional value to uniquely identify different terminals in the "
                                                   "store")
    store_name: Optional[str] = Field(description="Friendly name to help customer identify where the receipt came "
                                                  "from")

    address: Optional[Address] = Field(description="Store address to help customer identify where the receipt came "
                                                   "from")

    transaction_date: datetime = Field(default_factory=datetime.utcnow, description="Transaction date (UTC timezone)")

    amount: Decimal = Field(..., description="Total amount for this transaction. Include all taxes and discounts")
    currency: str = Field(..., description="The ISO-4217 code of the currency", regex="^[A-Z]{3}$")
    tax: Optional[Decimal]
    items: List[TransactionItem]
    payments: List[TransactionPayment]
    status: TransactionStatus = TransactionStatus.COMPLETED




