from fastapi import APIRouter, FastAPI
from fastapi.responses import JSONResponse

app: FastAPI = FastAPI()

router = APIRouter(prefix="/api/v0")


@router.get("/")
async def test() -> JSONResponse:
    return JSONResponse(content={"message": "test"})
