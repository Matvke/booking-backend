import logging

from fastapi import APIRouter, FastAPI

from app.user.user_router import user_router

app = FastAPI(
    version="0.0.1",
    title="booking-backend",
)
root_router = APIRouter(prefix="/api/v1")
root_router.include_router(user_router)

app.include_router(root_router)

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s (%(asctime)s):      %(message)s",
    datefmt="%d-%m-%Y %H:%M:%S",
)
