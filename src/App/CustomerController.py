from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials

from src.Model.APIBundle import APIBundle
from src.Model.APICustomer import APICustomer
from src.Model.APIItem import APIItem
from src.Model.Bundle import Bundle
from src.Model.Item import Item

from .init_app import customer_service, jwt_service, menu_service, order_service, stripe_service
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


@customer_router.put(
    "/me", status_code=status.HTTP_200_OK, dependencies=[Depends(CustomerBearer())]
)
def update_profile(
    customer_first_name: str = None,
    customer_last_name: str = None,
    customer_mail: str = None,
    customer_phone: str = None,
    customer_id: int = Depends(get_customer_id_from_token),
):
    try:
        update_data = locals()
        update_data.pop("customer_id")
        updated_customer = customer_service.update_customer(customer_id, update_data)
        return updated_customer

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating profile: {e}") from e


@customer_router.put(
    "/address", status_code=status.HTTP_200_OK, dependencies=[Depends(CustomerBearer())]
)
def update_address(
    address_number: int = None,
    address_street: str = None,
    address_city: str = None,
    address_postal_code: int = None,
    address_country: str = None,
    customer_id: int = Depends(get_customer_id_from_token),
):
    try:
        update_data = locals()
        update_data.pop("customer_id")
        print(update_data)
        print(type(update_data))
        updated_address = customer_service.update_address(customer_id, update_data)
        return updated_address

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating address: {e}") from e


@customer_router.put(
    "me/password", status_code=status.HTTP_200_OK, dependencies=[Depends(CustomerBearer())]
)
def update_password(
    current_password: str,
    new_password: str,
    confirm_password: str,
    customer_id: int = Depends(get_customer_id_from_token),
):
    try:
        if new_password != confirm_password:
            raise HTTPException(status_code=400, detail="")

        customer_service.update_password(customer_id, current_password, new_password)

        return "Password "

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error while changing password: {str(e)}"
        ) from e


@customer_router.get(
    "/menu", status_code=status.HTTP_200_OK, dependencies=[Depends(CustomerBearer())]
)
def get_menu():
    try:
        return menu_service.get_all_orderables()
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
    "/current-order",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(CustomerBearer())],
)
def get_order(
    order_id: int = Depends(get_current_order_id),
):
    return order_service.get_order_by_id(order_id)


@customer_router.put(
    "/current-order/{orderable_id}/add",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(CustomerBearer())],
)
def add_orderable_to_order(
    orderable_id: int,
    quantity: int,
    order_id: int = Depends(get_current_order_id),
):
    return order_service.add_orderable_to_order(orderable_id, order_id, quantity)


@customer_router.put(
    "/current-order/{orderable_id}/remove",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(CustomerBearer())],
)
def remove_orderable_from_order(
    orderable_id: int,
    quantity: int,
    order_id: int = Depends(get_current_order_id),
):
    return order_service.remove_orderable_from_order(orderable_id, order_id, quantity)


@customer_router.get(
    "/me/order_history", status_code=status.HTTP_200_OK, dependencies=[Depends(CustomerBearer())]
)
def view_order_history(customer_id: int = Depends(get_customer_id_from_token)):
    try:
        orders = order_service.get_all_orders_by_customer(customer_id)

        for order in orders:
            for i, content in enumerate(order.order_orderables):

                    if isinstance(content, Item):

                        order.order_orderables[i] = APIItem(
                            item_id=content.item_id,
                            orderable_id=content.orderable_id,
                            item_name=content.item_name,
                            item_price=content.item_price,
                            item_type=content.item_type,
                            item_description=content.item_description,
                        )

                    elif isinstance(content, Bundle):
                        for k, item in enumerate(content.bundle_items):
                            content.bundle_items[k] = APIItem(
                                item_id=item.item_id,
                                orderable_id=item.orderable_id,
                                item_name=item.item_name,
                                item_price=item.item_price,
                                item_type=item.item_type,
                                item_description=item.item_description,
                            )

                        order.order_orderables[i] = APIBundle(
                            bundle_id=content.bundle_id,
                            orderable_id=content.orderable_id,
                            bundle_name=content.bundle_name,
                            bundle_description=content.bundle_description,
                            bundle_items=content.bundle_items,
                        )
        return orders
    except Exception as e:
        raise Exception("[CustomerController] could not get order history") from e


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

        session_url = stripe_service.create_checkout_session(order, customer.customer_mail)

        return session_url

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to create checkout session: {e}"
        ) from e


@customer_router.get(
    "/payment/succes", status_code=status.HTTP_200_OK, dependencies=[Depends(CustomerBearer())]
)
def succesful_payment(session_id: int, order_id: int = Depends(get_current_order_id)):
    try:
        payment_info = stripe_service.verify_payment_status(session_id)

        if not payment_info["paid"]:
            raise HTTPException(
                status_code=400,
                detail=f"Payment not completed. Status: {payment_info['payment_status']}",
            )

        order_service.mark_as_paid(order_id)

        return order_service.get_order_by_id(order_id)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing payment: {e}") from e
