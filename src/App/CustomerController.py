from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials

# from traitlets.traitlets import isidentifier
from src.Model.APIBundle import APIBundle
from src.Model.APICustomer import APICustomer
from src.Model.APIItem import APIItem
from src.Model.Bundle import Bundle
from src.Model.Item import Item

from .init_app import (
    address_service,
    customer_service,
    jwt_service,
    menu_service,
    order_service,
    stripe_service,
)
from .JWTBearer import CustomerBearer

customer_router = APIRouter(
    prefix="/customer", tags=["Customers"], dependencies=[Depends(CustomerBearer())]
)


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
        updated_address = address_service.update_address(customer_id, update_data)
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


# @customer_router.get(
#     "/menu", status_code=status.HTTP_200_OK, dependencies=[Depends(CustomerBearer())]
# )
# def get_menu():
#     try:
#         menu = menu_service.get_all_orderables()
#         for i, content in enumerate(menu):
#             if isinstance(content, Item):
#                 menu[i] = APIItem(
#                     item_name=content.item_name,
#                     item_price=content.item_price,
#                     item_type=content.item_type,
#                     item_description=content.item_description,
#                 )

#             elif isinstance(content, Bundle):
#                 for key, value in content.bundle_items.items():
#                     items = {}
#                     items[
#                         APIItem(
#                             item_name=key.item_name,
#                             item_price=key.item_price,
#                             item_type=key.item_type,
#                             item_description=key.item_description,
#                         )
#                     ] = value

#                 menu[i] = APIBundle(
#                     bundle_name=content.bundle_name,
#                     bundle_description=content.bundle_description,
#                     bundle_items=items,
#                 )
#         return menu

#     except ValueError as e:
#         raise HTTPException(status_code=400, detail=str(e)) from e
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error updating profile: {e}") from e


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
    # Modif Néo comme pour history


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
    if quantity <= 0:
        errortext = "[CustomerController] Invalid input:"
        errortext += " cannot add 0 or a negative number of orderables."
        raise HTTPException(
            status_code=403,
            detail=errortext,
        )
    try:
        return order_service.add_orderable_to_order(orderable_id, order_id, quantity)
    except Exception as e:
        raise HTTPException(
            status_code=403, detail=f"[CustomerController] cannot add orderable : {str(e)}"
        ) from e


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
    if quantity <= 0:
        errortext = "[CustomerController] Invalid input:"
        errortext += " cannot remove 0 or a negative number of orderables."
        raise HTTPException(
            status_code=403,
            detail=errortext,
        )
    try:
        return order_service.remove_orderable_from_order(orderable_id, order_id, quantity)
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

        for order in orders:
            history = {}
            for key, value in order.order_orderables.items():
                if isinstance(key, Item):
                    history[
                        APIItem(
                            item_name=key.item_name,
                            item_price=key.item_price,
                            item_type=key.item_type,
                            item_description=key.item_description,
                        )
                    ] = value

                elif isinstance(key, Bundle):
                    for key2, value2 in key.bundle_items.items():
                        items = {}
                        items[
                            APIItem(
                                item_name=key2.item_name,
                                item_price=key2.item_price,
                                item_type=key2.item_type,
                                item_description=key2.item_description,
                            )
                        ] = value2

                    history[
                        APIBundle(
                            bundle_name=key.bundle_name,
                            bundle_description=key.bundle_description,
                            bundle_items=items,
                        )
                    ] = value

            order.order_orderables = history
        return orders
    except Exception as e:
        raise Exception("[CustomerController] Could not get order history") from e


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


# PROBLEME : Les objets custom comme clé de dict ne sont jamais automatiquement convertis en JSON.
# Pour un affichage lisible avec des virgules (JSON),
# il faudrait utiliser une string ou un tuple comme clé.
# Peut-être : prendre les élèments voulus et faire un tuple (mais APIBunde & APIIteam dégage)


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
def succesful_payment(
    session_id,
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
