from fastapi import APIRouter, HTTPException, Response
from Requests.EmployeeRequest import EmployeeAuth, EmployeeRegister
from Models.Employee import User, Employee
from jwtFunctions import write_token
from dotenv import load_dotenv
from Models.Store import Store
from fastapi import Depends
from jwtFunctions import verify_manager_access, verify_credentials


employee_routes = APIRouter()
load_dotenv()


@employee_routes.post("/login")
async def login(user: EmployeeAuth, response: Response):
    info = verify_credentials(user)
    token = write_token(info)
    response.set_cookie(key="token_c", value=token, httponly=True)
    return {"message": "Login successful", "token": token}


@employee_routes.post("/logout")
async def logout(response: Response):
    response.delete_cookie(key="token")
    return {"message": "Logout successful"}


@employee_routes.post("/register", dependencies=[Depends(verify_manager_access)])
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
