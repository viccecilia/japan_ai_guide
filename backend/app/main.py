from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.routers import chat, history, language, spots
from app.schemas.api_response import error_response

app = FastAPI(title="Japan AI Guide API", version="0.0.1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:3000", "http://localhost:3000"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.router)
app.include_router(spots.router)
app.include_router(history.router)
app.include_router(language.router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "japan-ai-guide"}


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(
    request: Request,
    exc: StarletteHTTPException,
) -> JSONResponse:
    payload = error_response(
        code=f"HTTP_{exc.status_code}",
        message=str(exc.detail),
        meta={"path": request.url.path},
    )
    return JSONResponse(status_code=exc.status_code, content=payload.model_dump())


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    payload = error_response(
        code="VALIDATION_ERROR",
        message="Request validation failed.",
        meta={"path": request.url.path, "detail_count": len(exc.errors())},
    )
    return JSONResponse(status_code=422, content=payload.model_dump())
