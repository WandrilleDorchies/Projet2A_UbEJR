from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials

from src.Model.Customer import Customer

from .init_app import customer_service, jwt_service
from .JWTBearer import JWTBearer

customer_router = APIRouter(prefix="/customer", tags=["Customers"])


@customer_router.get("/me", dependencies=[Depends(JWTBearer())])
def get_user_own_profile(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(JWTBearer())],
) -> Customer | None:
    """
    Get the authenticated user profile
    """
    return get_customer_from_credentials(credentials)


def get_customer_from_credentials(credentials: HTTPAuthorizationCredentials) -> Customer:
    token = credentials.credentials
    customer_id = int(jwt_service.validate_user_jwt(token))
    customer: Customer | None = customer_service.get_customer_by_id(customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="[CustomerController] User not found")
    return customer


@customer_router.get(
    "/me/order_history",
    dependencies=[Depends(JWTBearer())],
    status_code=status.HTTP_200_OK,
)
def view_order_history(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(JWTBearer())],
):
    # get user / customer from credentials a creer
    current_customer: Customer = get_customer_from_credentials(credentials)
    try:
        customer_service.order_history(current_customer.id)
    except Exception:
        print("[CustomerController] could not get order history")
