import logging
import logging.config
import os

from fastapi import FastAPI
from fastapi.routing import APIRoute
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware

from app.api.main import api_router
from app.core.config import settings

# Configure logging
logging.config.fileConfig("logging.conf", disable_existing_loggers=False)
logger = logging.getLogger("sampleLogger")
logger.info("Application started")

logger.info(f"Current working directory: {os.getcwd()}")


def custom_generate_unique_id(route: APIRoute) -> str:
    if route.tags:
        return f"{route.tags[0]}-{route.name}"
    else:
        return f"default-{route.name}"


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    generate_unique_id_function=custom_generate_unique_id,
)

# Mount the static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(api_router, prefix="/api/v1")

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            str(origin).strip("/") for origin in settings.BACKEND_CORS_ORIGINS
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


@app.get("/")
async def root():
    logging.getLogger("sampleLogger").debug("Test log message from the root route")
    return {"message": "Hello World"}


@app.get("/test-static")
async def test_static():
    static_dir = "static"
    files = os.listdir(static_dir)
    logger.info(f"Static directory contents: {files}")
    return {"static_files": files}


app.include_router(api_router, prefix=settings.API_V1_STR)
