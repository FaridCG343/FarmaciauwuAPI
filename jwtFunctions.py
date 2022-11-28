from jwt import encode, decode, exceptions
from datetime import datetime, timedelta
from os import getenv
from dotenv import load_dotenv
from fastapi.responses import JSONResponse
from fastapi import Cookie, HTTPException, Depends


load_dotenv()


def expire_date(days: int):
    date = datetime.now()
    new_date = date + timedelta(days)
    return new_date


def write_token(data: dict):
    token = encode(payload={**data, "exp": expire_date(1)}, key=getenv("SECRET"))
    return token


async def validate_token(token: str = Cookie(None)):
    if token is None:
        raise HTTPException(302, {"message": "Please login"})
    try:
        return decode(token, key=getenv("SECRET"), algorithms=["HS256"])
    except exceptions.DecodeError:
        raise HTTPException(detail={"message": "Invalid token"}, status_code=401)
    except exceptions.ExpiredSignatureError:
        raise HTTPException(detail={"message": "token expired"}, status_code=401)


async def verify_inventory_manager_access(user_data=Depends(validate_token)):
    if not user_data["position"] == "Inventory Manager":
        raise HTTPException(401)
    return user_data


async def verify_cashier_access(user_data=Depends(validate_token)):
    if user_data["position"] not in ["Cashier", "Supervisor", "Manager"]:
        raise HTTPException(401)
    return user_data
