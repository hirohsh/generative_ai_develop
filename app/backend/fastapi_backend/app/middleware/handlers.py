import json

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import ORJSONResponse

from app.config.base_config import PRODUCTION_FLUG
from app.schemas.error_response_schema import ErrorDetail, ErrorJsonResponse


def add_exception_handlers(app: FastAPI) -> None:
    # カスタムエラーハンドラの定義
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException) -> ORJSONResponse:
        # 本番環境では詳細を隠し、ステータスコードを 500 に統一
        status_code = 500 if PRODUCTION_FLUG else exc.status_code
        error_detail = "Internal Server Error" if PRODUCTION_FLUG else exc.detail
        type_name = "server_error" if PRODUCTION_FLUG else "http_error"

        error = ErrorJsonResponse(
            detail=[ErrorDetail(loc=[f"{request.method} {request.url.path}"], msg=error_detail, type=type_name)]
        )
        return ORJSONResponse(status_code=status_code, content=error.model_dump())

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError) -> ORJSONResponse:
        # 本番環境では詳細を隠し、ステータスコードを 500 に統一
        status_code = 500 if PRODUCTION_FLUG else 422
        error_detail = "Internal Server Error" if PRODUCTION_FLUG else json.dumps(exc.errors())
        type_name = "server_error" if PRODUCTION_FLUG else "validation_error"

        error = ErrorJsonResponse(
            detail=[ErrorDetail(loc=[f"{request.method} {request.url.path}"], msg=error_detail, type=type_name)]
        )
        return ORJSONResponse(status_code=status_code, content=error.model_dump())
