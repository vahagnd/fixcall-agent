
"""Routes module."""

from fastapi import FastAPI

from routers import (
    telegram,
    debug,
)


def init_routers(app: FastAPI):
    app.include_router(telegram.router)
    app.include_router(debug.router)
