from fastapi import FastAPI

from app.routers import router

app: FastAPI = FastAPI()

app.include_router(router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)  # noqa: S104
