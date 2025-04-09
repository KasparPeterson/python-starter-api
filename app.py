from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware

import settings
from src import api_logger
from src.routers import main_router

logger = api_logger.get()


@asynccontextmanager
async def lifespan(_: FastAPI):
    # Initialise global settings and start background jobs
    # my_env.load()
    # my_background_job.start()
    yield

    # Clean up resources and database before shutting down
    logger.info("Shutdown Signal received. Cleaning up...")

    # Shut down my background jobs gracefully...
    # my_background_job.stop()

    logger.info("Cleanup complete.")


app = FastAPI(lifespan=lifespan)

app.include_router(
    main_router.router,
)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="API",
        version="1.0.0",
        description="API version 1.0.0",
        routes=app.routes,
        servers=_get_servers(),
    )
    openapi_schema["info"]["contact"] = {"name": "", "email": ""}
    openapi_schema["info"]["x-logo"] = {"url": ""}
    openapi_schema["x-readme"] = {
        "samples-languages": ["curl", "node", "javascript", "python"]
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


def _get_servers():
    servers = []
    if settings.is_production():
        base_url = settings.API_BASE_URL
        if base_url.endswith("/"):
            base_url = base_url[:-1]
        servers.append({"url": base_url})
    else:
        base_url = settings.API_BASE_URL
        if base_url.endswith("/"):
            base_url = base_url[:-1]
        servers.append({"url": f"{base_url}:{settings.API_PORT}"})
    return servers


app.openapi = custom_openapi

# order of middleware matters! first middleware called is the last one added
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_TITLE = "Python Starter API"
API_DESCRIPTION = "Python Starter API"


class ApiInfo(BaseModel):
    title: str
    description: str

    class Config:
        json_schema_extra = {
            "example": {
                "title": API_TITLE,
                "description": API_DESCRIPTION,
            }
        }


def get_api_info() -> ApiInfo:
    return ApiInfo(title=API_TITLE, description=API_DESCRIPTION)


@app.get(
    "/",
    summary="Returns API information",
    description="Returns API information",
    response_description="API information with title and description.",
    response_model=ApiInfo,
)
async def root():
    return get_api_info()
