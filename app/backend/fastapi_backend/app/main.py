from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from app.routers import router

app: FastAPI = FastAPI(default_response_class=ORJSONResponse)

app.include_router(router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)  # noqa: S104
