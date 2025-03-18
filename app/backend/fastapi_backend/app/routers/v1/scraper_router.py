"""
scraper用のルーティングを定義する。
"""

import logging
from typing import Annotated

from fastapi import APIRouter, Body

from app.schemas.scraper_schema import TechbizParam, TechbizTaskPostResponse
from app.services.scrapy.mappings import TECHBIZ_TARGET_MAPPING

router = APIRouter(prefix="/scraper", tags=["Scraper"])

logger = logging.getLogger(__name__)


@router.post("/techbiz")
async def add_task_techbiz(param: Annotated[TechbizParam, Body(..., description="テックビズクローラー用パラメーター", embed=False)]) -> TechbizTaskPostResponse:
    # スキル名に対応するエンドポイント名を取得
    mapped_name: str | None = TECHBIZ_TARGET_MAPPING.get(param.target) if param.target else None

    return TechbizTaskPostResponse(task_id=mapped_name, message="Crawl task started.")
