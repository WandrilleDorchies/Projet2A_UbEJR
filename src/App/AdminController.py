from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials

from .init_app import (
    jwt_service,
    menu_service,
    # item_service,
    # bundle_service,
    # customer_service,
    # driver_service,
    # order_service,
)
from .JWTBearer import AdminBearer

admin_router = APIRouter(prefix="/admin", tags=["Admin"], dependencies=[Depends(AdminBearer())])


# ITEMS
def get_admin_id_from_token(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(AdminBearer())],
) -> int:
    token = credentials.credentials
    customer_id = int(jwt_service.validate_user_jwt(token))
    return customer_id


@admin_router.get(
    "/orderables", status_code=status.HTTP_200_OK, dependencies=[Depends(AdminBearer())]
)
def get_all_orderables():
    try:
        return menu_service.get_all_orderable(in_menu=False)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching orderables: {e}") from e
