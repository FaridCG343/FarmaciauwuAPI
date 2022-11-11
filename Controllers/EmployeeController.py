from fastapi import APIRouter
from Requests.EmployeeRequest import EmployeeAuth
from Models.Employee import User
from jwtFunctions import write_token
from fastapi.responses import JSONResponse

employee_routes = APIRouter()


@employee_routes.post("/login")
async def login(user: EmployeeAuth):
    em = User.select().where(User.employee_id == user.id).first()
    if em:
        if em.getinfo()["password"] == user.password:
            if em.getinfo()["is_admin"]:
                user.admin = 1
            else:
                user.admin = 0
            return write_token(user.dict())
        else:
            return JSONResponse(content={"message": "incorrect password"}, status_code=401)
    else:
        return JSONResponse(content={"message": "Employee not found"}, status_code=404)