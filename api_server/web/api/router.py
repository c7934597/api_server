from fastapi.routing import APIRouter

from api_server.web.api import monitoring, main

api_router = APIRouter()
api_router.include_router(monitoring.router)
api_router.include_router(main.router, prefix="/main", tags=["main"])
