from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from app.middleware.handlers import add_exception_handlers
from app.middleware.middleware import EnhancedTracebackMiddleware
from app.routers import router

load_dotenv()

app: FastAPI = FastAPI(default_response_class=ORJSONResponse)

# エラーハンドラーの登録
add_exception_handlers(app)

# ミドルウェアの登録
app.add_middleware(EnhancedTracebackMiddleware)

# ルーターの追加
app.include_router(router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)  # noqa: S104
