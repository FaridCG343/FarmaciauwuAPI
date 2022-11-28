from os import getenv
from fastapi import APIRouter, HTTPException, Response
from Requests.EmployeeRequest import EmployeeAuth, EmployeeRegister
from Models.Employee import User, Employee
from jwtFunctions import write_token
from fastapi.responses import JSONResponse
from cryptography.fernet import Fernet
from dotenv import load_dotenv
from Models.Store import Store


employee_routes = APIRouter()
load_dotenv()
key = getenv("SALT")
fernet = Fernet(key.encode())


@employee_routes.post("/login")
async def login(user: EmployeeAuth, response: Response):
    em = User.select().where(User.employee_id == user.id).dicts()
    if em:
        em = em[0]
        store = Store.select().\
            where(Store.id == em["store_id"]).\
            first()
        if not store.active:
            raise HTTPException(401, {"message": "The store is inactive"})
        if fernet.decrypt(em["password"].encode()).decode() == user.password:
            info = {
                "employee": em["employee_id"],
                "position": em["position"],
                "store": em["store_id"]
            }
            token = write_token(info)
            response.set_cookie(key="token", value=token, httponly=True)
            return {"message": "Login successful"}
        else:
            return JSONResponse(content={"message": "incorrect password"}, status_code=401)
    else:
        return JSONResponse(content={"message": "Employee not found"}, status_code=404)


@employee_routes.post("/logout")
async def logout(response: Response):
    response.delete_cookie(key="token")
    return {"message": "Logout successful"}


@employee_routes.post("/register")
async def register(new_user: EmployeeRegister):
    store = Store.select().where(Store.id == new_user.store).first()
    if store is None:
        raise HTTPException(404, "The store was not found")
    new_employee = Employee.create(
        name=new_user.name,
        lastname=new_user.lastname,
        phoneNumber=new_user.phone_number
    )
    password = fernet.encrypt(new_user.password.encode())
    User.create(
        employee_id=new_employee.id,
        password=password,
        position=new_user.position,
        store_id=store.id
    )
    return {"message": "New user has been created", "userNumber": f"{new_employee.id}"}
