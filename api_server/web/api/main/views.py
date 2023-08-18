import time

from loguru import logger

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from API_Server.web.api.main.schema import Item
from API_Server.services.image_inference import Inference

router = APIRouter()


@router.post("/inference")
async def inference(item: Item) -> JSONResponse:
    try:
        since = time.perf_counter()
        result = Inference.run(item.models_name_list, item.file_path)
        time_elapsed = time.perf_counter() - since
        logger.debug(str(round(time_elapsed * 1000, 2)) + "ms")
        logger.debug(result)
        return result
    except Exception as e:
        logger.error(e)
        return str(e)
