from enum import Enum
from typing import Type

import boto3
from fastapi import Body, Depends, HTTPException
from mypy_boto3_bedrock_runtime import BedrockRuntimeClient

from app.interfaces.bedrock_interface import BedrockModelBase, ConfigTypeDef, InvokeRequestTypeDef
from app.services.bedrock.llama_service import LLAMA_CONFIG, LlamaService


class ModelType(str, Enum):
    """モデルの種類を表す列挙型"""

    LLAMA3 = "Llama3"


# マッピング定義
MODEL_MAPPING: dict[ModelType, Type[BedrockModelBase]] = {ModelType.LLAMA3: LlamaService}

CONFIG_MAPPING: dict[ModelType, ConfigTypeDef] = {ModelType.LLAMA3: LLAMA_CONFIG}


# Query定義
MODEL_TYPE_QUERY: ModelType = Body(..., description="使用するモデルの種類", embed=True)
USER_INPUT_QUERY: InvokeRequestTypeDef = Body(..., description="ユーザーの入力", embed=True)


# 依存関数定義
def get_bedrock_client() -> BedrockRuntimeClient:
    """bedrock用ランタイムクライアントを返す

    Returns:
        BedrockRuntimeClient: bedrock用ランタイムクライアント
    """
    return boto3.client(service_name="bedrock-runtime", region_name="us-east-1")


def get_model_service(model_type: ModelType = MODEL_TYPE_QUERY) -> BedrockModelBase:
    """
    クエリパラメータからEnumを利用してインスタンスを取得

    Args:
        model_type (ModelType): モデルの種類

    Raises:
        HTTPException: 無効なmodel_typeが指定された場合に、HTTP 400エラーを発生させる。

    Returns:
        BedrockModelBase: 指定されたモデルタイプに対応するサービスインスタンス
    """
    model_service: Type[BedrockModelBase] | None = MODEL_MAPPING.get(model_type)
    config: ConfigTypeDef | None = CONFIG_MAPPING.get(model_type)

    if model_service is None or config is None:
        raise HTTPException(status_code=400, detail="無効なモデルタイプが指定されました")

    return model_service.from_dependency(client=get_bedrock_client(), config=config)


# Depends定義
MODEL_SERVICE_DEPENDS: BedrockModelBase = Depends(get_model_service, use_cache=False)
