import uvicorn
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from src.utils.log_init import initialiser_logs

from .AdminController import admin_router
from .AuthentificationController import auth_router
from .CustomerController import customer_router
from .DriverController import driver_router


def run_app():
    app = FastAPI(title="Projet Info 2A", description="Example project for ENSAI students")

    initialiser_logs("Projet Ub'EJR Eats")

    @app.get("/", include_in_schema=False)
    async def redirect_to_docs():
        """Redirect to the API documentation"""
        return RedirectResponse(url="/docs")

    app.include_router(auth_router)
    app.include_router(customer_router)
    app.include_router(driver_router)
    app.include_router(admin_router)
    uvicorn.run(app, port=8000, host="0.0.0.0")
