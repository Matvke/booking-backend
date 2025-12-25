from app.core.exceptions import AlreadyExistsError, NotFoundError


class UserAlreadyExistsError(AlreadyExistsError):
    def __init__(self, detail="The user already exists."):
        super().__init__(detail)


class UserNotFoundError(NotFoundError):
    def __init__(self, key, value, detail="The requested user not found."):
        super().__init__(key, value, detail)
