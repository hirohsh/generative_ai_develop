from fastapi import APIRouter

from app.routers.v1 import bedrock

router = APIRouter(prefix="/v1")

router.include_router(bedrock.router, tags=["V1 Bedrock"])
