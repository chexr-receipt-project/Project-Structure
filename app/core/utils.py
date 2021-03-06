from decimal import Decimal

__NUM_DIGITS__ = 10


def decimal_encoder (val: Decimal) -> str:
    return str(round(val, __NUM_DIGITS__))


CHEXR_ENCODER = {
    Decimal: decimal_encoder
}

