from chexr.core.database import get_database
from chexr.bank.bank_repository import find_bank_by_client_id
from chexr.merchant.merchant_repository import find_merchant_by_client_id
from fastapi import Header, HTTPException, Depends
from typing import Optional
import jwt


async def get_logged_bank(authorization: Optional[str] = Header(None), database=Depends(get_database)):
    return await _get_user(
        authorization,
        "receipts/bank",
        lambda client_id: find_bank_by_client_id(database, client_id)
    )


async def get_logged_merchant(authorization: Optional[str] = Header(None), database=Depends(get_database)):
    return await _get_user(
        authorization,
        "receipts/merchant",
        lambda client_id: find_merchant_by_client_id(database, client_id)
    )


async def verify_admin(authorization: Optional[str] = Header(None)):
    await _validade_user(authorization, "receipts/admin")


async def _get_user(authorization: str, mandatory_scope: str, find_user_correct_context):
    client_id = await _validade_user(authorization, mandatory_scope)

    user = await find_user_correct_context(client_id)

    if user is None:
        raise HTTPException(status_code=401, detail=f"Client id '{client_id}' not associated to a user")

    return user


async def _validade_user(authorization, mandatory_scope):
    if authorization is None:
        raise HTTPException(status_code=401, detail="No Authentication provided")
    authorization = authorization[len("bearer "):]
    decoded_authorization = jwt.decode(authorization, options={"verify_signature": False})
    client_id = decoded_authorization['sub']
    authorization_scope = decoded_authorization['scope']
    if mandatory_scope != authorization_scope:
        raise HTTPException(status_code=403, detail="missing scope")
    return client_id
