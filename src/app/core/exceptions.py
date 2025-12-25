from typing import Any

from fastapi import status
from fastapi.exceptions import HTTPException


class NotFoundError(HTTPException):
    def __init__(self, key: str, value: Any, detail="The requested entity not found."):
        self.key = key
        self.value = value
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{detail} {self.key} = {self.value}",
        )


class AlreadyExistsError(HTTPException):
    def __init__(self, detail="The entity already exists."):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"{detail}",
        )
