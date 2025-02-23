"""
Bedrock モデルで使用する型定義および設定値の構造を定義する。
"""

from enum import Enum
from typing import Generic, NotRequired, TypedDict, TypeVar

from fastapi import UploadFile
from mypy_boto3_bedrock_runtime.type_defs import (
    ConverseRequestRequestTypeDef,
    ConverseStreamRequestRequestTypeDef,
    InvokeModelRequestRequestTypeDef,
    InvokeModelWithResponseStreamRequestRequestTypeDef,
)

###############################################################
# 共通
###############################################################

T = TypeVar("T")

InvokeRequestTypeDef = str | bytes | UploadFile  # invoke_modelのリクエストで受け取るパラメーターの型


class ModelType(str, Enum):
    """モデルの種類を表す列挙型"""

    LLAMA3 = "Llama3"


class SdkConfigTypeDef(TypedDict):
    """
    Bedrockランタイムクライアントの各メソッドで使用する設定の型定義
    """

    invoke: NotRequired[InvokeModelRequestRequestTypeDef]  # invoke_model
    invoke_stream: NotRequired[InvokeModelWithResponseStreamRequestRequestTypeDef]  # invoke_model_with_response_stream
    converse: NotRequired[ConverseRequestRequestTypeDef]  # converse
    converse_stream: NotRequired[ConverseStreamRequestRequestTypeDef]  # converse_stream


class ConfigTypeDef(TypedDict, Generic[T]):
    """
    モデルサービスで使用する設定の型定義
    """

    sdk: SdkConfigTypeDef
    model: NotRequired[T]


###############################################################
# Llama3
###############################################################


class LlamaInvokeRequestModelConfigTypeDef(TypedDict):
    """
    Llama3のinvoke_modelに使用するパラメーター型定義
    """

    prompt: str
    temperature: float
    top_p: float
    max_gen_len: int


class LlamaInvokeRequestStreamModelConfigTypeDef(TypedDict):
    """
    Llama3のinvoke_model_streamに使用するパラメーター型定義
    """

    prompt: str
    temperature: float
    top_p: float
    max_gen_len: int


class LlamaConfigTypeDef(TypedDict):
    """
    Llama3サービス 各種メソッドのモデル自体に渡すパラメーター型定義
    """

    invoke: LlamaInvokeRequestModelConfigTypeDef
    invoke_stream: LlamaInvokeRequestStreamModelConfigTypeDef
