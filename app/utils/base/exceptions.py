from fastapi import status, HTTPException


class BadRequestError(Exception):
    pass


class UnauthorizedError(Exception):
    pass


class NotFoundError(Exception):
    pass


class ServerError(Exception):
    pass


credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid or expired token",
    headers={"WWW-Authenticate": "Bearer"},
)