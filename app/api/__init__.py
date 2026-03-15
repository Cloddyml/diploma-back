from fastapi import APIRouter

from app.api.topics import admin_router as admin_topics_router
from app.api.topics import router as topics_router

routers: list[APIRouter] = [
    topics_router,
    admin_topics_router,
]
