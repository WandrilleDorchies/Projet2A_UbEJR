from typing import Annotated

import phonenumbers as pn
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials

from .init_app import customer_service, jwt_service, menu_service
from .JWTBearer import CustomerBearer

customer_router = APIRouter(
    prefix="/customer", tags=["Customers"], dependencies=[Depends(CustomerBearer())]
)


# def get_customer_from_credentials(credentials: HTTPAuthorizationCredentials) -> APICustomer:
#     token = credentials.credentials
#     customer_id = int(jwt_service.validate_user_jwt(token))
#     customer: Customer | None = customer_service.get_customer_by_id(customer_id)
#     if not customer:
#         raise HTTPException(status_code=404, detail="[CustomerController] Customer not found")
#     return APICustomer(
#         id=customer.id,
#         first_name=customer.first_name,
#         last_name=customer.last_name,
#         address=customer.customer_address,
#     )
# @customer_router.get("/me")
# def get_user_own_profile(
#     credentials: Annotated[HTTPAuthorizationCredentials, Depends(CustomerBearer)],
# ) -> APICustomer:
#     """
#     Get the authenticated user profile
#     """
#     return get_customer_from_credentials(credentials)


def get_customer_id_from_token(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(CustomerBearer())],
) -> int:
    token = credentials.credentials
    customer_id = int(jwt_service.validate_user_jwt(token))
    return customer_id


@customer_router.get(
    "/me", status_code=status.HTTP_200_OK, dependencies=[Depends(CustomerBearer())]
)
def get_profile(customer_id: int = Depends(get_customer_id_from_token)):
    try:
        customer = customer_service.get_customer_by_id(customer_id)
        return customer
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching profile: {e}") from e


@customer_router.put(
    "/me", status_code=status.HTTP_200_OK, dependencies=[Depends(CustomerBearer())]
)
def update_profile(
    first_name: str = None,
    last_name: str = None,
    mail: str = None,
    phone: str = None,
    customer_id: int = Depends(get_customer_id_from_token),
):
    try:
        update_data = {}
        if first_name:
            update_data["customer_first_name"] = first_name
        if last_name:
            update_data["customer_last_name"] = last_name
        if mail:
            update_data["customer_mail"] = mail

        if phone:
            phone_number = pn.parse(phone, "FR")
            if not pn.is_valid_number(phone_number) or not pn.is_possible_number(phone_number):
                raise ValueError(f"The number {phone} is invalid.")

            customer_phone = "0" + str(phone_number.national_number)
            update_data["customer_phone"] = customer_phone

        updated_customer = customer_service.update_customer(customer_id, update_data)
        return updated_customer

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating profile: {e}") from e


@customer_router.get(
    "/menu", status_code=status.HTTP_200_OK, dependencies=[Depends(CustomerBearer())]
)
def get_menu():
    try:
        return menu_service.get_all_orderable_in_menu()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating profile: {e}") from e


@customer_router.get(
    "/menu/{orderable_id}", status_code=status.HTTP_200_OK, dependencies=[Depends(CustomerBearer())]
)
def get_orderable_detail(orderable_id: int):
    try:
        return menu_service.get_orderable_from_menu(orderable_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating profile: {e}") from e


@customer_router.get(
    "/orders", status_code=status.HTTP_200_OK, dependencies=[Depends(CustomerBearer())]
)
def get_all_orders(customer_id: int = Depends(get_customer_id_from_token)):
    pass


@customer_router.get(
    "/orders/{order_id}", status_code=status.HTTP_200_OK, dependencies=[Depends(CustomerBearer())]
)
def get_order(order_id: int, customer_id: int = Depends(get_customer_id_from_token)):
    pass


@customer_router.post(
    "/orders/{order_id}/{orderable_id}",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(CustomerBearer())],
)
def add_orderable_to_order(
    orderable_id: int,
    order_id: int,
    customer_id: int = Depends(get_customer_id_from_token),
):
    pass


# @customer_router.get(
#     "/me/order_history",
#     status_code=status.HTTP_200_OK,
# )
# def view_order_history(
#     credentials: Annotated[HTTPAuthorizationCredentials, Depends(CustomerBearer)],
# ):
#     current_customer: Customer = get_customer_from_credentials(credentials)
#     try:
#         customer_service.order_history(current_customer.id)
#     except Exception:
#         print("[CustomerController] could not get order history")
