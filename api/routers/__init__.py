"""Routes module."""

from fastapi import FastAPI

from routers import (
    debug,
    telegram,
)


def init_routers(app: FastAPI):  # noqa: ANN201
    app.include_router(telegram.router)
    app.include_router(debug.router)
