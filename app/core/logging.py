import logging
import logging.config

from app.core.config import settings

_LOG_FORMAT = "%(asctime)s [%(levelname)s] %(name)s — %(message)s"
_DATE_FORMAT = "%H:%M:%S"


def setup_logging() -> None:
    """Единый dictConfig для приложения, Celery и сторонних библиотек."""
    level = "DEBUG" if settings.MODE in {"LOCAL", "DEV"} else "INFO"

    logging.config.dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "default": {
                    "format": _LOG_FORMAT,
                    "datefmt": _DATE_FORMAT,
                },
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "formatter": "default",
                },
            },
            "root": {
                "level": level,
                "handlers": ["console"],
            },
            "loggers": {
                "uvicorn.access": {"level": "WARNING"},
                "sqlalchemy.engine": {"level": "WARNING"},
            },
        }
    )
