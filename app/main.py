from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse

from .routers import router
from .core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION
)

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

app.include_router(router)

@app.get("/")
async def root():
    return {"message": "Hello World"}