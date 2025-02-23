# マッピング定義
from typing import Annotated, Type

import boto3
from fastapi import Body, Depends, HTTPException
from mypy_boto3_bedrock_runtime import BedrockRuntimeClient

from app.config.bedrock_config import LLAMA_CONFIG
from app.interfaces.bedrock_interface import BedrockModelBase
from app.services.bedrock.llama_service import LlamaService
from app.types.bedrock_type_defs import ConfigTypeDef, ModelType

MODEL_MAPPING: dict[ModelType, Type[BedrockModelBase]] = {ModelType.LLAMA3: LlamaService}

CONFIG_MAPPING: dict[ModelType, ConfigTypeDef] = {ModelType.LLAMA3: LLAMA_CONFIG}


# 依存関数定義
def get_bedrock_client() -> BedrockRuntimeClient:
    """bedrock用ランタイムクライアントを返す

    Returns:
        BedrockRuntimeClient: bedrock用ランタイムクライアント
    """
    return boto3.client(service_name="bedrock-runtime", region_name="us-east-1")


def get_model_service(
    model_type: Annotated[ModelType, Body(..., description="使用するモデルの種類", embed=True)],
) -> BedrockModelBase:
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
MODEL_SERVICE_DEPENDS = Depends(get_model_service, use_cache=False)
