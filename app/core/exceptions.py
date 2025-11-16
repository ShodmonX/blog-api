from fastapi import HTTPException
from starlette.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_409_CONFLICT
)


def bad_request(detail: str = "Bad request"):
    raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=detail)

def unauthorized(detail: str = "Unauthorized"):
    raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail=detail)

def forbidden(detail: str = "Forbidden"):
    raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail=detail)

def not_found(detail: str = "Not found"):
    raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=detail)

def conflict(detail: str = "Bad request"):
    raise HTTPException(status_code=HTTP_409_CONFLICT, detail=detail)
