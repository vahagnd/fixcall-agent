
"""Routes module."""

from fastapi import FastAPI

from routers import (
    webhooks,
    debug,
)


def init_routers(app: FastAPI):  # noqa: ANN201
    app.include_router(webhooks.router)
    app.include_router(debug.router)
