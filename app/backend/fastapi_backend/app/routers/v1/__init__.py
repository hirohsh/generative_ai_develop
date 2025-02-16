from fastapi import APIRouter

from app.routers.v1 import bedrock_router

router = APIRouter(prefix="/v1")

router.include_router(bedrock_router.router, tags=["V1 Bedrock"])
