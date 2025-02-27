import logging
from logging.config import dictConfig
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from app.config.logging_config import LOG_DIR_NAME, LOGGING_CONFIG
from app.middleware.handlers import add_exception_handlers
from app.middleware.middleware import EnhancedTracebackMiddleware
from app.routers import router

load_dotenv()

app: FastAPI = FastAPI(default_response_class=ORJSONResponse)

# ログ保管用ディレクトリ作成
if not Path.exists(LOG_DIR_NAME):
    Path.mkdir(LOG_DIR_NAME)

# ロギングの設定
dictConfig(LOGGING_CONFIG)

# エラーハンドラーの登録
add_exception_handlers(app)

# ミドルウェアの登録
app.add_middleware(EnhancedTracebackMiddleware)

# ルーターの追加
app.include_router(router)

logger = logging.getLogger(__name__)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, log_config=LOGGING_CONFIG)  # noqa: S104
