from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from src.App.init_app import (
    customer_service,
    driver_service,
    menu_service,
    order_service,
)
from src.App.JWTBearer import AdminBearer
from src.Model.Order import OrderState

templates = Jinja2Templates(directory="templates")
admin_router = APIRouter(prefix="", tags=["General"], dependencies=[Depends(AdminBearer())])


# OVERVIEW
@admin_router.get(
    "/overview", status_code=status.HTTP_200_OK, dependencies=[Depends(AdminBearer())]
)
def get_overview():
    try:
        # customers = customer_service.get_all_customers()
        # drivers = driver_service.get_all_drivers()

        benef = order_service.get_benef()
        orders_count = order_service.get_number_orders_by_state()

        nb_items = menu_service.get_number_of_orderables()

        return {
            # "total_customers": len(customers) if customers else 0,
            # "total_drivers": len(drivers) if drivers else 0,
            "total_orderables_in_menu": nb_items,
            "total_orders_ready": orders_count["ready_for_delivering"],
            "total_orders_in_kitchen": orders_count["preparing"],
            "benefice": f"{benef} €",
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching datas: {e}") from e


@admin_router.get("/logout", response_class=HTMLResponse)
async def logout(request: Request):
    response = RedirectResponse("/", status_code=302)
    response.delete_cookie(key="access_token")
    return templates.TemplateResponse("auth.html", {"request": request})
