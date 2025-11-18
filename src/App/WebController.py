from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from .CustomerController import get_customer_id_from_token
from .init_app import customer_service, menu_service

templates = Jinja2Templates(directory="templates")

web_router = APIRouter(tags=["Web Interface"])


@web_router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("auth.html", {"request": request})


@web_router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("auth.html", {"request": request})


@web_router.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse("auth.html", {"request": request, "active_tab": "register"})


@web_router.get("/menu", response_class=HTMLResponse)
async def menu_page(request: Request, user_id: int = Depends(get_customer_id_from_token)):
    try:
        user = customer_service.get_customer_by_id(user_id)
        orderables = menu_service.get_all_orderables()
        items = []
        bundles = []
        item_types = []

        for o in orderables:
            if o.orderable_type == "item":
                items.append(o)
                item_types.append(o.item_type)
            else:
                bundles.append(o)

        return templates.TemplateResponse(
            "menu.html",
            {
                "request": request,
                "items": items,
                "bundles": bundles,
                "item_types": set(item_types),
                "user": user,
            },
        )
    except Exception as e:
        print(f"Erreur lors du chargement du menu: {e}")
        return templates.TemplateResponse(
            "menu.html",
            {"request": request, "items": [], "bundles": [], "item_types": []},
        )


@web_router.get("/logout", response_class=HTMLResponse)
async def logout(request: Request):
    response = RedirectResponse("auth.html", status_code=302)
    response.delete_cookie(key="access_token")
    return templates.TemplateResponse("auth.html", {"request": request})
