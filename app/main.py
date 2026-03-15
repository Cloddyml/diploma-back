import uvicorn
from fastapi import FastAPI

from app.core.config import settings
from app.core.lifespan import lifespan
from app.core.routes import add_routers

app = FastAPI(
    lifespan=lifespan,
)
add_routers(app)


def main():

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.MODE != "PROD",
    )


if __name__ == "__main__":
    main()
