from fastapi import APIRouter, HTTPException, status

from src.App.init_app import customer_service, jwt_service, user_service
from src.Model.JWTResponse import JWTResponse

from typing import Literal

auth_router = APIRouter(prefix="/auth", tags=["Authentication"])


@auth_router.post("/register", status_code=status.HTTP_201_CREATED)
def register(
    first_name: str,
    last_name: str,
    phone: str,
    mail: str,
    password: str,
    address_string: str,
):
    try:
        customer = customer_service.create_customer(
            first_name, last_name, phone, mail, password, address_string
        )

        jwt_token = jwt_service.encode_jwt(customer.id)

        return {
            "user": {
                "id": customer.id,
                "first_name": customer.first_name,
                "last_name": customer.last_name,
                "phone": customer.customer_phone,
                "email": customer.customer_mail,
                "hash_pw": customer.customer_hashed_password,
                "type": "customer",
            },
            "access_token": jwt_token.access_token,
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Registration failed: {e}") from e


@auth_router.post("/login", status_code=status.HTTP_200_OK)
def login(
    identifier: str, password: str, user_type: Literal["admin", "customer", "driver"]
) -> JWTResponse:
    try:
        if user_type not in ("admin", "customer", "driver"):
            raise HTTPException(
                status_code=400, detail="Invalid user_type. Must be: customer, driver, or admin"
            )

        user = user_service.login(identifier=identifier, password=password, user_type=user_type)

        token = jwt_service.encode_jwt(user.id)

        return token

    except ValueError as e:
        raise HTTPException(status_code=401, detail="Invalid credentials") from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Login failed: {e}") from e
