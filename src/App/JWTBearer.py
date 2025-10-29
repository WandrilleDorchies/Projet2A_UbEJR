from fastapi import HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import DecodeError, ExpiredSignatureError
from src.DAO.AdminDAO import AdminDAO
from src.DAO.CustomerDAO import CustomerDAO
from src.DAO.DriverDAO import DriverDAO

from .init_app import jwt_service


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials:
        credentials: HTTPAuthorizationCredentials | None = await super(JWTBearer, self).__call__(
            request
        )
        if not credentials:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

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
    admin_dao: AdminDAO

    def __init__(self, admin_dao: AdminDAO):
        self.admin_dao = admin_dao

    async def __call__(self, request: Request):
        credentials = await super().__call__(request)
        user_id = jwt_service.validate_user_jwt(credentials.credentials)

        user = self.admin_dao.get_admin(user_id)
        if user.user_role != "admin":
            raise HTTPException(403, "You need to be an admin to access this page.")

        return credentials


class CustomerBearer(JWTBearer):
    customer_dao: CustomerDAO

    def __init__(self, customer_dao: CustomerDAO):
        self.customer_dao = customer_dao

    async def __call__(self, request: Request):
        credentials = await super().__call__(request)
        user_id = jwt_service.validate_user_jwt(credentials.credentials)

        user = self.customer_dao.get_driver_by_id(user_id)
        if user.user_role != "customer":
            raise HTTPException(403, "You need to be a customer to access this page.")

        return credentials


class DriverBearer(JWTBearer):
    driver_dao: DriverDAO

    def __init__(self, driver_dao: DriverDAO):
        self.driver_dao = driver_dao

    async def __call__(self, request: Request):
        credentials = await super().__call__(request)
        user_id = jwt_service.validate_user_jwt(credentials.credentials)

        user = self.driver_dao.get_driver_by_id(user_id)
        if user.user_role != "driver":
            raise HTTPException(403, "You need to be a driver to access this page.")

        return credentials
