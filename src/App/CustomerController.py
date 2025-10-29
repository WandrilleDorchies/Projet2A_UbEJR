from typing import TYPE_CHECKING, Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials

from src.Model.Customer import Customer

from .init_app import customer_service, user_service
from .JWTBearer import CustomerBearer, JWTBearer

customer_router = APIRouter(prefix="/customer", tags=["Customers"])

"""
@customer_router.get(
    "/me/order_history",
    dependencies=[Depends(CustomerBearer())],
    status_code=status.HTTP_200_OK,
)
def view_order_history(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(CustomerBearer())],
):
    # get user / customer from credentials a creer
    current_customer: Customer = user_service.get_customer_from_credentials(credentials)
    try:
        customer_service.order_history(current_customer.id)
    except Exception:
        print("could not get order history")
"""
