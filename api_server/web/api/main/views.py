import time

from loguru import logger

from anyio.lowlevel import RunVar
from anyio import CapacityLimiter

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from api_server.settings import settings
from api_server.web.api.main.schema import Item
from api_server.services.image_inference import Image_Inference

router = APIRouter()
image_inference = Image_Inference()


@router.on_event("startup")
def startup():
    RunVar("_default_thread_limiter").set(CapacityLimiter(settings.capacity_limiter))

@router.post("/inference")
async def inference(item: Item) -> JSONResponse:
    try:
        since = time.perf_counter()
        result = image_inference.run(item.models_name_list, item.file_path)
        time_elapsed = time.perf_counter() - since
        logger.debug(str(round(time_elapsed * 1000, 2)) + "ms")
        logger.debug(result)
        return result
    except Exception as e:
        logger.error("Exception: {}".format(str(e)))
        return JSONResponse(status_code=500, content={"message": "Internal Server Error"})
