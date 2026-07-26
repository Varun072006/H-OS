"""HumanOS FastAPI Application Factory."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api.router import api_router
from backend.config import settings


def create_app() -> FastAPI:
    """Instantiate and configure FastAPI application."""
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description="HumanOS REST & WebSocket API for Privacy-First Human Motion Intelligence",
        openapi_url=f"{settings.api_prefix}/openapi.json",
        docs_url=f"{settings.api_prefix}/docs",
        redoc_url=f"{settings.api_prefix}/redoc",
    )

    # CORS Middleware configuration
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Mount main API router under prefix /v1
    app.include_router(api_router, prefix=settings.api_prefix)

    return app


app = create_app()
