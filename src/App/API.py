import uvicorn
from fastapi import FastAPI

from .MovieController import movie_router
from .UserController import user_router


def run_app():
    app = FastAPI(title="Projet Info 2A", description="Example project for ENSAI students")

    app.include_router(user_router)

    app.include_router(movie_router)

    uvicorn.run(app, port=9876, host="localhost")
