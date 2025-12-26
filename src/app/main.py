import logging

from fastapi import APIRouter, Depends, FastAPI

from app.core import settings
from app.core.auth import bot_auth
from app.specialist.specialist_router import specialist_router
from app.user.user_router import user_router

app = FastAPI(
    version="0.0.2",
    title="booking-backend",
)
if settings.DEBUG:
    root_router = APIRouter(prefix="/api/v1")
else:
    root_router = APIRouter(prefix="/api/v1", dependencies=[Depends(bot_auth)])

root_router.include_router(user_router)
root_router.include_router(specialist_router)

app.include_router(root_router)


logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s (%(asctime)s):      %(message)s",
    datefmt="%d-%m-%Y %H:%M:%S",
)
