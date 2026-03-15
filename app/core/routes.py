from fastapi import FastAPI

from app.api import routers
from app.core.config import settings


def add_routers(app: FastAPI):
    for router in routers:
        app.include_router(router, prefix=f"/api/{settings.API_VERSION}")
