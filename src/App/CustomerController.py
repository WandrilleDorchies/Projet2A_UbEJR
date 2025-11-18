from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials
from pydantic import BaseModel

from src.Model.APICustomer import APICustomer
from src.Model.Bundle import Bundle
from src.Model.Item import Item

from .init_app import (
    address_service,
    customer_service,
    jwt_service,
    order_service,
    stripe_service,
)
from .JWTBearer import CustomerBearer

customer_router = APIRouter(
    prefix="/customer", tags=["Customers"], dependencies=[Depends(CustomerBearer())]
)


class AddRemoveOrderable(BaseModel):
    orderable_id: int
    quantity: int


# PROFILE
def get_customer_id_from_token(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(CustomerBearer())],
) -> int:
    token = credentials.credentials
    customer_id = int(jwt_service.validate_user_jwt(token)["user_id"])
    return customer_id


def get_current_order_id(
    customer_id: int = Depends(get_customer_id_from_token),
) -> int:
    order = order_service.get_customer_current_order(customer_id)
    if order is None:
        raise HTTPException(status_code=404, detail="The order wasn't created")

    return order.order_id


@customer_router.get(
    "/me", status_code=status.HTTP_200_OK, dependencies=[Depends(CustomerBearer())]
)
def get_profile(customer_id: int = Depends(get_customer_id_from_token)) -> APICustomer:
    try:
        customer = customer_service.get_customer_by_id(customer_id)
        return APICustomer(
            id=customer.id,
            first_name=customer.first_name,
            last_name=customer.last_name,
            address=customer.customer_address,
            customer_phone=customer.customer_phone,
            customer_mail=customer.customer_mail,
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching profile: {e}") from e


class CustomerUpdate(BaseModel):
    customer_first_name: str = None
    customer_last_name: str = None
    customer_mail: str = None
    customer_phone: str = None


@customer_router.put(
    "/me", status_code=status.HTTP_200_OK, dependencies=[Depends(CustomerBearer())]
)
def update_profile(
    customer_update: CustomerUpdate,
    customer_id: int = Depends(get_customer_id_from_token),
):
    try:
        update_data = vars(customer_update)
        updated_customer = customer_service.update_customer(customer_id, update_data)
        return updated_customer

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating profile: {e}") from e


class AdressUpdate(BaseModel):
    address_number: int = None
    address_street: str = None
    address_city: str = None
    address_postal_code: int = None
    address_country: str = None


@customer_router.put(
    "/address", status_code=status.HTTP_200_OK, dependencies=[Depends(CustomerBearer())]
)
def update_address(
    address_update: AdressUpdate,
    customer_id: int = Depends(get_customer_id_from_token),
):
    try:
        update_data = vars(address_update)
        updated_address = address_service.update_address(customer_id, update_data)
        return updated_address

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating address: {e}") from e


class PasswordUpdate(BaseModel):
    current_password: str
    new_password: str
    confirm_password: str


@customer_router.put(
    "me/password", status_code=status.HTTP_200_OK, dependencies=[Depends(CustomerBearer())]
)
def update_password(
    password_update: PasswordUpdate,
    customer_id: int = Depends(get_customer_id_from_token),
):
    try:
        if password_update.new_password != password_update.confirm_password:
            raise HTTPException(status_code=400, detail="")

        customer_service.update_password(
            customer_id, password_update.current_password, password_update.new_password
        )

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error while changing password: {str(e)}"
        ) from e


@customer_router.get(
    "/current-order",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(CustomerBearer())],
)
def get_order(
    order_id: int = Depends(get_current_order_id),
):
    order = order_service.get_order_by_id(order_id)
    return {
        "order_id": order.order_id,
        "order_price": order.order_price,
        "order_orderables": {
            orderable.orderable_id: quantity
            for orderable, quantity in order.order_orderables.items()
        },
    }


@customer_router.put(
    "/current-order/add",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(CustomerBearer())],
)
def add_orderable_to_order(
    add_orderable: AddRemoveOrderable,
    order_id: int = Depends(get_current_order_id),
):
    if add_orderable.quantity <= 0:
        errortext = "[CustomerController] Invalid input:"
        errortext += " cannot add 0 or a negative number of orderables."
        raise HTTPException(
            status_code=403,
            detail=errortext,
        )
    try:
        return order_service.add_orderable_to_order(
            add_orderable.orderable_id, order_id, add_orderable.quantity
        )
    except Exception as e:
        raise HTTPException(
            status_code=403, detail=f"[CustomerController] cannot add orderable : {str(e)}"
        ) from e


@customer_router.put(
    "/current-order/remove",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(CustomerBearer())],
)
def remove_orderable_from_order(
    add_orderable: AddRemoveOrderable,
    order_id: int = Depends(get_current_order_id),
):
    if add_orderable.quantity <= 0:
        errortext = "[CustomerController] Invalid input:"
        errortext += " cannot remove 0 or a negative number of orderables."
        raise HTTPException(
            status_code=403,
            detail=errortext,
        )
    try:
        return order_service.remove_orderable_from_order(
            add_orderable.orderable_id, order_id, add_orderable.quantity
        )
    except Exception as e:
        raise HTTPException(
            status_code=403,
            detail="[CustomerController] Invalid input: "
            f"cannot remove orderable from order - {str(e)}",
        ) from e


@customer_router.get(
    "/me/order_history", status_code=status.HTTP_200_OK, dependencies=[Depends(CustomerBearer())]
)
def view_order_history(customer_id: int = Depends(get_customer_id_from_token)):
    try:
        orders = order_service.get_all_orders_by_customer(customer_id)
        history = []

        for order in orders:
            orderables_list = []

            for orderable, qty in order.order_orderables.items():
                if isinstance(orderable, Item):
                    orderables_list.append(
                        {
                            "item_name": orderable.item_name,
                            "item_price": orderable.item_price,
                            "quantity": qty,
                            "type": "item",
                        }
                    )

                elif isinstance(orderable, Bundle):
                    orderables_list.append(
                        {
                            "bundle_name": orderable.bundle_name,
                            "bundle_price": orderable.bundle_price,
                            "quantity": qty,
                            "type": "bundle",
                        }
                    )

            formatted_order = {
                "order_id": order.order_id,
                "order_timestamp": str(order.order_timestamp),
                "order_state": str(order.order_state),
                "order_price": order.order_price,
                "items": orderables_list,
            }

            history.append(formatted_order)

        return history

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"[CustomerController] Could not get order history: {str(e)}"
        ) from e


@customer_router.delete(
    "/delete_account",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(CustomerBearer())],
)
def delete_account(identifier: str, password: str):
    try:
        customer = customer_service.login_customer(identifier, password)
        return customer_service.delete_customer(customer.id)

    except ValueError as e:
        raise HTTPException(status_code=401, detail=f"Invalid credentials: {e}") from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Login failed: {e}") from e


# PAYMENT
@customer_router.post(
    "/payment/checkout",
    status_code=status.HTTP_202_ACCEPTED,
    dependencies=[Depends(CustomerBearer())],
)
def create_checkout_session(
    order_id: int = Depends(get_current_order_id),
    customer_id: int = Depends(get_customer_id_from_token),
):
    try:
        order = order_service.get_order_by_id(order_id)

        if order.is_paid:
            raise HTTPException(status_code=400, detail="Order is already paid.")

        customer = customer_service.get_customer_by_id(customer_id)

        return stripe_service.create_checkout_session(order, customer.customer_mail)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to create checkout session: {e}"
        ) from e


@customer_router.post(
    "/payment/verify-payment",
    status_code=status.HTTP_202_ACCEPTED,
    dependencies=[Depends(CustomerBearer())],
)
def verify_payment(
    session_id: str,
    customer_id: int = Depends(get_customer_id_from_token),
    order_id: int = Depends(get_current_order_id),
):
    try:
        payment_info = stripe_service.verify_payment(session_id)

        if not payment_info["paid"]:
            raise HTTPException(
                status_code=400,
                detail=f"Payment not completed. Status: {payment_info['payment_status']}",
            )

        order_service.mark_as_paid(order_id)
        order_service.create_order(customer_id)

        return order_service.get_order_by_id(order_id)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing payment: {e}") from e
