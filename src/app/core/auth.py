from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core import settings

security = HTTPBearer()


async def bot_auth(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> None:
    bot_token = credentials.credentials
    if not bot_token:
        raise HTTPException(403, "Missing authorization token")
    if not validate_token(bot_token):
        raise HTTPException(403, "Invalid or expired token")


def validate_token(bot_token):
    # TODO У каждого бота будет свой токен.
    return bot_token == settings.API_SECRET_KEY
