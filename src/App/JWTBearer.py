from fastapi import HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import DecodeError, ExpiredSignatureError

from .init_app import admin_dao, customer_dao, driver_dao, jwt_service


class JWTBearer(HTTPBearer):
    def __init__(
        self,
        # auto_error: bool = False
    ):
        super(JWTBearer, self).__init__(auto_error=False)

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials:
        credentials: HTTPAuthorizationCredentials | None = await super(JWTBearer, self).__call__(
            request
        )
        if not credentials:
            token = request.cookies.get("access_token")
            if token:
                credentials = HTTPAuthorizationCredentials(scheme="Bearer", credentials=token)

        if not credentials.scheme == "Bearer":
            raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
        try:
            jwt_service.validate_user_jwt(credentials.credentials)
        except ExpiredSignatureError as e:
            raise HTTPException(status_code=403, detail="Expired token") from e
        except DecodeError as e:
            raise HTTPException(status_code=403, detail="Error decoding token") from e
        except Exception as e:
            raise HTTPException(status_code=403, detail="Unknown error") from e

        return credentials


class AdminBearer(JWTBearer):
    async def __call__(self, request: Request):
        credentials = await super().__call__(request)
        user_id = jwt_service.validate_user_jwt(credentials.credentials)

        user = admin_dao.get_admin(user_id)
        if user.user_role != "admin":
            raise HTTPException(403, "You need to be an admin to access this page.")

        return credentials


class CustomerBearer(JWTBearer):
    async def __call__(self, request: Request):
        credentials = await super().__call__(request)
        user_id = jwt_service.validate_user_jwt(credentials.credentials)

        user = customer_dao.get_customer_by_id(user_id)
        if user.user_role != "customer":
            raise HTTPException(403, "You need to be a customer to access this page.")

        return credentials


class DriverBearer(JWTBearer):
    async def __call__(self, request: Request):
        credentials = await super().__call__(request)
        user_id = jwt_service.validate_user_jwt(credentials.credentials)

        user = driver_dao.get_driver_by_id(user_id)
        if user.user_role != "driver":
            raise HTTPException(403, "You need to be a driver to access this page.")

        return credentials
