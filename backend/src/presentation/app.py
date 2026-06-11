import sentry_sdk
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka

from src.core.config import settings
from src.presentation.api.v1 import include_router
from src.presentation.di.providers import make_base_providers
from src.presentation.exception_handlers import register_exception_handlers
from src.presentation.middlewares.rate_limit import RateLimitingMiddleware


def create_app() -> FastAPI:
    if settings.app.sentry_dsn:
        sentry_sdk.init(
            dsn=settings.app.sentry_dsn,
            traces_sample_rate=0.1,
        )

    app = FastAPI(
        title="Timekeep API",
        description="API for timekeeping",
        version="1.0.0",
        prefix="/api",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.app.allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    container = make_async_container(
        *make_base_providers(),
    )

    setup_dishka(container, app)

    register_exception_handlers(app)
    app.add_middleware(RateLimitingMiddleware)

    include_router(app)

    # setup_logging()

    return app
