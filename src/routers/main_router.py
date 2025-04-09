from typing import List

from fastapi import APIRouter

from src.routers.routes import my_router

TAG_ROOT = "root"

router = APIRouter(prefix="/v0")

routers_to_include: List[APIRouter] = [
    # This is the order they show up in openapi.json
    my_router.router
]

for router_to_include in routers_to_include:
    router.include_router(router_to_include)
