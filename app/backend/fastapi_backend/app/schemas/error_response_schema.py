"""
エラーに関するレスポンススキーマを定義する。
"""

from typing import List

from pydantic import BaseModel, Field


class ErrorDetail(BaseModel):
    loc: List[str] = Field(..., description="エラー箇所")
    msg: str = Field(..., description="エラーメッセージ")
    type: str = Field(..., description="エラータイプ")

    model_config = {
        "json_schema_extra": {
            "example": {
                "loc": ["body", "name"],
                "msg": "1文字以上である必要があります。",
                "type": "value_error",
            }
        }
    }


class ErrorJsonResponse(BaseModel):
    detail: List[ErrorDetail] = Field(..., description="エラーメッセージ")
