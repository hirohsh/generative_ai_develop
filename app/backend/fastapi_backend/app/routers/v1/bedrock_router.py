from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/bedrock", tags=["Bedrock"])


@router.get("/")
def test() -> JSONResponse:
    return JSONResponse(content={"message": "test"})
