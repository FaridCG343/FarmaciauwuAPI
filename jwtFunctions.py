from jwt import encode, decode, exceptions
from datetime import datetime, timedelta
from os import getenv
from dotenv import load_dotenv
from fastapi import Cookie, HTTPException, Depends, Header
from cryptography.fernet import Fernet
from Models.Employee import User
from Models.Store import Store


load_dotenv()


def expire_date(days: int):
    date = datetime.now()
    new_date = date + timedelta(days)
    return new_date


def write_token(data: dict):
    token = encode(payload={**data, "exp": expire_date(1)}, key=getenv("SECRET"))
    return token


async def validate_token(token_c: str = Cookie(None), token_h: str = Header(None)):
    if token_c is None:
        if token_h is None:
            raise HTTPException(302, {"message": "Please login"})
        token = token_h
    else:
        token = token_c
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


async def verify_manager_access(user_data=Depends(validate_token)):
    if user_data["position"] not in ["Manager"]:
        raise HTTPException(401)
    return user_data


async def verify_supervisor_access(user_data=Depends(validate_token)):
    if user_data["position"] not in ["Supervisor", "Manager"]:
        raise HTTPException(401)
    return user_data


def verify_credentials(user):
    key = getenv("SALT")
    fernet = Fernet(key.encode())
    em = User.select().where(User.employee_id == user.id).dicts()
    if em:
        em = em[0]
        store = Store.select(). \
            where(Store.id == em["store_id"]). \
            first()
        if not store.active:
            raise HTTPException(401, {"message": "The store is inactive"})
        if fernet.decrypt(em["password"].encode()).decode() == user.password:
            info = {
                "employee": em["employee_id"],
                "position": em["position"],
                "store": em["store_id"]
            }
            return info
        else:
            raise HTTPException(detail={"message": "incorrect password"}, status_code=401)
    else:
        raise HTTPException(detail={"message": "Employee not found"}, status_code=404)
