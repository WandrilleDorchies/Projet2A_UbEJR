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

templates = Jinja2Templates(directory="templates")
admin_router = APIRouter(prefix="", tags=["General"], dependencies=[Depends(AdminBearer())])


# OVERVIEW
@admin_router.get(
    "/overview", status_code=status.HTTP_200_OK, dependencies=[Depends(AdminBearer())]
)
def get_overview():
    try:
        customers = customer_service.get_all_customers()
        drivers = driver_service.get_all_drivers()
        orders = order_service.get_all_orders()
        orders_prepared = order_service.get_prepared_orders()
        current_orders = order_service.get_current_orders()
        benef = [order.order_price for order in order_service.get_past_orders()]
        items = menu_service.get_all_orderables(in_menu=True)

        return {
            "total_customers": len(customers) if customers else 0,
            "total_drivers": len(drivers) if drivers else 0,
            "total_orders": len(orders) if orders else 0,
            "total_orders_prepared": len(orders_prepared) if orders_prepared else 0,
            "total_current_orders": len(current_orders) if current_orders else 0,
            "total_orderables_in_menu": len(items) if items else 0,
            "benefice": f"{sum(benef)} €",
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching datas: {e}") from e


@admin_router.get("/logout", response_class=HTMLResponse)
async def logout(request: Request):
    response = RedirectResponse("/", status_code=302)
    response.delete_cookie(key="access_token")
    return templates.TemplateResponse("auth.html", {"request": request})
