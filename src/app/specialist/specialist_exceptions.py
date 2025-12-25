from fastapi import status
from fastapi.exceptions import HTTPException

from app.core.exceptions import AlreadyExistsError, NotFoundError


class SpecialistAlreadyExistsError(AlreadyExistsError):
    def __init__(self, detail="The specialist already exists."):
        super().__init__(detail)


class SpecialistNotFoundError(NotFoundError):
    def __init__(self, key, value, detail="The requested specialist not found."):
        super().__init__(key, value, detail)


class SpecialistVerificationError(HTTPException):
    def __init__(self, detail="Invalid invitation token"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


class SpecialistHasNoTelegramError(HTTPException):
    def __init__(self, detail="The specialist does't have Telegram."):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail,
        )
