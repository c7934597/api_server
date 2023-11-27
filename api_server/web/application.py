from importlib import metadata

from fastapi import FastAPI
from fastapi.responses import UJSONResponse
from fastapi.middleware.cors import CORSMiddleware

from debug_toolbar.middleware import DebugToolbarMiddleware

from api_server.settings import settings
from api_server.logging import configure_logging
from api_server.web.api.router import api_router
from api_server.web.lifetime import register_shutdown_event, register_startup_event

# 根據環境變量決定是否開啟debug模式
is_debug = settings.environment == "dev"


def get_app() -> FastAPI:
    """
    Get FastAPI application.

    This is the main constructor of an application.

    :return: application.
    """
    configure_logging()
    app = FastAPI(
        title="api_server",
        description="Provide Member Sync & Update Operations",
        version=metadata.version("api_server"),
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        openapi_url="/api/openapi.json",
        default_response_class=UJSONResponse,
        debug=is_debug,
    )

    if is_debug:
        app.add_middleware(
            DebugToolbarMiddleware,
        )
    else:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    # Adds startup and shutdown events.
    register_startup_event(app)
    register_shutdown_event(app)

    # Main router for the API.
    app.include_router(router=api_router, prefix="/api")

    return app
