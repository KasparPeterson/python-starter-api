from fastapi import APIRouter

from src import api_logger
from pydantic import BaseModel
from pydantic import Field

TAG = "MyRouter"
router = APIRouter(prefix="/my_route")
router.tags = [TAG]

logger = api_logger.get()


class MyResponse(BaseModel):
    response: str = Field(description="My response", default="Hello World")


@router.get(
    "/",
    summary="Example endpoint",
    description="",
    response_description="Example description",
    response_model=MyResponse,
)
async def get():
    logger.debug("example log")
    return MyResponse(response="Hello World")
