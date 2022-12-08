from fastapi import APIRouter, HTTPException, Response, Depends
from Requests.EmployeeRequest import EmployeeAuth, EmployeeRegister, EmployeeUpdate
from Models.Employee import User, Employee
from jwtFunctions import write_token, encrypt_password
from Models.Store import Store
from fastapi.responses import JSONResponse
from jwtFunctions import verify_manager_access, verify_credentials
from responseHelper import *


employee_routes = APIRouter(tags=['Employee'])


@employee_routes.post("/register", dependencies=[Depends(verify_manager_access)], responses={
    200: set_custom_response("OK", {"message": "New user has been created"}),
    401: set_401_response(),
    404: set_404_response(),
    409: set_409_response()
})
async def register(new_user: EmployeeRegister):
    store = Store.select().where(Store.id == new_user.store).first()
    if store is None:
        raise HTTPException(404, detail={"message": "The store was not found"})
    existing_employee = Employee.select().where(Employee.phoneNumber == new_user.phone_number).first()
    if existing_employee:
        raise HTTPException(409, detail={"message": "The phone number is already in use"})
    new_employee = Employee.create(
        name=new_user.name,
        lastname=new_user.lastname,
        phoneNumber=new_user.phone_number
    )
    password = encrypt_password(new_user.password)
    User.create(
        employee_id=new_employee.id,
        password=password,
        position=new_user.position,
        store_id=store.id
    )
    return {"message": "New user has been created"}


@employee_routes.put("/{employee_id}", dependencies=[Depends(verify_manager_access)])
async def change_password(employee_id: str, new_password: EmployeeUpdate):
    user = User.select().where(User.employee_id == employee_id).first()
    if user is None:
        raise HTTPException(404, detail={"message": "User not found"})
    password = encrypt_password(new_password.password)
    User.update({User.password: password}).where(User.employee_id == employee_id).execute()
    return JSONResponse({"message": "Password changed successfully"})
