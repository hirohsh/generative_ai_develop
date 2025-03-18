"""
スクレイパーに関するレスポンススキーマを定義する。
"""

from typing import Any

from pydantic import BaseModel

from app.types.scraper_type_defs import TechbizMenuSkills


class TechbizParam(BaseModel):
    """
    テックビズリクエスト時のパラメータ
    """

    target: TechbizMenuSkills | None = None


class TechbizTaskPostResponse(BaseModel):
    """
    テックビズタスク登録リクエストのレスポンス
    """

    task_id: Any | None
    message: str
