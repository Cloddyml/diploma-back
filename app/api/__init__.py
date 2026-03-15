from fastapi import APIRouter

from app.api.topics import router as topics_router

routers: list[APIRouter] = [
    topics_router,
]
