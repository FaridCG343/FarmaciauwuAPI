from fastapi import APIRouter, HTTPException, Response, Depends
from Requests.EmployeeRequest import EmployeeAuth, EmployeeRegister, EmployeeUpdate
from Models.Employee import User, Employee
from jwtFunctions import write_token, encrypt_password
from Models.Store import Store
from fastapi.responses import JSONResponse
from jwtFunctions import verify_manager_access, verify_credentials
from responseHelper import *


employee_routes = APIRouter(tags=['Employee'])


@employee_routes.post("/login", responses={
    200: set_custom_response("OK", {"message": "Login successful", "token": "token_uwu"}),
    400: set_custom_response("Bad request", {"detail": {"message": "Incorrect password"}}),
    404: set_404_response()
})
async def login(user: EmployeeAuth, response: Response):
    info = verify_credentials(user)
    token = write_token(info)
    response.set_cookie(key="token_c", value=token, httponly=True)
    return {"message": "Login successful", "token": token}


@employee_routes.post("/logout")
async def logout(response: Response):
    response.delete_cookie(key="token")
    return {"message": "Logout successful"}


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
    existing_user = User.select().where(User.userName == new_user.username).first()
    if existing_user:
        raise HTTPException(409, detail={"message": "The username is already in use"})
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
        store_id=store.id,
        userName=new_user.username.lower()
    )
    return {"message": "New user has been created"}


@employee_routes.put("/{username}", dependencies=[Depends(verify_manager_access)])
async def change_password(username: str, new_password: EmployeeUpdate):
    user = User.select().where(User.userName == username).first()
    if user is None:
        raise HTTPException(404, detail={"message": "User not found"})
    password = encrypt_password(new_password.password)
    User.update({User.password: password}).where(User.userName == username).execute()
    return JSONResponse({"message": "Password changed successfully"})
