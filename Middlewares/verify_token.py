from fastapi import Request
from jwtFunctions import validate_token
from fastapi.routing import APIRoute


class VerifyToken(APIRoute):
    def get_route_handler(self):
        original_route = super().get_route_handler()

        async def verify_token_middleware(request: Request):
            token = request.headers["Authorization"].split(" ")[1]
            validation = validate_token(token)
            if validation is None:
                return await original_route(request)
            else:
                return validation
        return verify_token_middleware
