from typing import Any, MutableMapping

from fastapi.responses import ORJSONResponse
from starlette.types import ASGIApp, Receive, Scope, Send

from app.config.base_config import PRODUCTION_FLUG
from app.schemas.error_response_schema import ErrorDetail, ErrorJsonResponse


class EnhancedTracebackMiddleware:
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        # HTTP以外のスコープはそのまま通す
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        response_started = False

        # send関数をラップして、レスポンス開始のタイミングを検知する
        async def send_wrapper(message: MutableMapping[str, Any]) -> None:
            nonlocal response_started
            if message["type"] == "http.response.start":
                response_started = True
            await send(message)

        try:
            # アプリケーション呼び出し(ストリーミング処理中の例外もここでキャッチ可能)
            await self.app(scope, receive, send_wrapper)
        except Exception:
            # すでにレスポンスが開始されている場合は、エラーレスポンスを送信できないため再送出
            if response_started:
                raise
            # 本番環境では詳細情報を隠す
            error_detail = "Internal Server Error" if PRODUCTION_FLUG else ""

            error = ErrorJsonResponse(
                detail=[
                    ErrorDetail(
                        loc=[f"{scope.get('method', 'UNKNOWN')} {scope.get('path', '')}"],
                        msg=error_detail,
                        type="server_error",
                    )
                ]
            )
            response = ORJSONResponse(status_code=500, content=error.model_dump())
            await response(scope, receive, send)
