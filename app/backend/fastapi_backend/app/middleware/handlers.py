import json
import logging

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import ORJSONResponse

from app.config.base_config import PRODUCTION_FLAG
from app.schemas.error_response_schema import ErrorDetail, ErrorJsonResponse

logger = logging.getLogger(__name__)


def add_exception_handlers(app: FastAPI) -> None:
    # カスタムエラーハンドラの定義
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException) -> ORJSONResponse:
        # ログ出力
        logger.exception("An http error occurred!")
        # 本番環境では詳細を隠し、ステータスコードを 500 に統一
        status_code = 500 if PRODUCTION_FLAG else exc.status_code
        error_detail = "Internal Server Error" if PRODUCTION_FLAG else exc.detail
        type_name = "server_error" if PRODUCTION_FLAG else "http_error"

        error = ErrorJsonResponse(
            detail=[ErrorDetail(loc=[f"{request.method} {request.url.path}"], msg=error_detail, type=type_name)]
        )
        return ORJSONResponse(status_code=status_code, content=error.model_dump())

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError) -> ORJSONResponse:
        # ログ出力
        logger.exception("An validation error occurred!")
        # 本番環境では詳細を隠し、ステータスコードを 500 に統一
        status_code = 500 if PRODUCTION_FLAG else 422
        error_detail = "Internal Server Error" if PRODUCTION_FLAG else json.dumps(exc.errors())
        type_name = "server_error" if PRODUCTION_FLAG else "validation_error"

        error = ErrorJsonResponse(
            detail=[ErrorDetail(loc=[f"{request.method} {request.url.path}"], msg=error_detail, type=type_name)]
        )
        return ORJSONResponse(status_code=status_code, content=error.model_dump())
