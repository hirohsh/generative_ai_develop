"""
bedrock用のルーティングを定義する。
"""

from typing import TYPE_CHECKING, Annotated, AsyncGenerator

from fastapi import APIRouter, Body, HTTPException
from fastapi.responses import ORJSONResponse, StreamingResponse

from app.schemas.bedrock_schema import MessageList

if TYPE_CHECKING:
    from collections.abc import Sequence

    from mypy_boto3_bedrock_runtime.type_defs import BlobTypeDef, MessageTypeDef, MessageUnionTypeDef

from app.dependencies.bedrock_dependencies import MODEL_SERVICE_DEPENDS
from app.interfaces.bedrock_interface import (
    BedrockModelBase,
    ISupportsConverse,
    ISupportsConverseStream,
    ISupportsInvokeModel,
    ISupportsInvokeModelStream,
)

router = APIRouter(prefix="/bedrock", tags=["Bedrock"])


@router.post("/converse")
async def converse(
    user_input: Annotated[MessageList, Body(..., description="ConverseAPI用のユーザー入力", embed=True)],
    bedrock_service: Annotated[BedrockModelBase, MODEL_SERVICE_DEPENDS],
) -> ORJSONResponse:
    """
    Converse API 用エンドポイント。
    ユーザーの入力に基づいて対話応答を返す。

    Args:
        bedrock_service (Annotated[BedrockModelBase, MODEL_SERVICE_DEPENDS]):
            モデルサービスのインスタンス。各種モデル固有の処理を提供する。
        user_input (Annotated[MessageList, Body, optional):
            ユーザーからの会話入力。

    Raises:
        HTTPException: 指定されたモデルが Converse API に対応していない、もしくは入力が無効な場合。

    Returns:
        ORJSONResponse: モデルからの応答を含むレスポンス。
    """
    if not isinstance(bedrock_service, ISupportsConverse):
        raise HTTPException(status_code=400, detail="このモデルは対応してません")

    converse_messages: Sequence[MessageUnionTypeDef] = bedrock_service.generate_converse_messages(user_input)
    reply_text: str = await bedrock_service.converse(converse_messages)
    return ORJSONResponse(content=reply_text)


@router.post("/converse/stream")
async def converse_stream(
    user_input: Annotated[MessageList, Body(..., description="ConverseAPI用のユーザー入力", embed=True)],
    bedrock_service: Annotated[BedrockModelBase, MODEL_SERVICE_DEPENDS],
) -> StreamingResponse:
    """
    Converse Stream API 用エンドポイント。
    ユーザーの入力に基づいてストリーミングで対話応答を返す。

    Args:
        bedrock_service (Annotated[BedrockModelBase, MODEL_SERVICE_DEPENDS]):
            モデルサービスのインスタンス。各種モデル固有の処理を提供する
        user_input (Annotated[MessageList, Body, optional):
            ユーザーからの会話入力。

    Raises:
        HTTPException: 指定されたモデルが Converse API に対応していない、もしくは入力が無効な場合。

    Returns:
        StreamingResponse: ストリーミングで対話応答を含むレスポンス。
    """
    if not isinstance(bedrock_service, ISupportsConverseStream):
        raise HTTPException(status_code=400, detail="このモデルは対応してません")

    converse_messages: Sequence[MessageTypeDef] = bedrock_service.generate_converse_stream_messages(user_input)
    stream_generator: AsyncGenerator[str, None] = bedrock_service.converse_stream(converse_messages)
    return StreamingResponse(stream_generator, media_type="text/plain")


@router.post("/invoke-model")
async def invoke_model(
    user_input: Annotated[MessageList, Body(..., description="ユーザーの入力", embed=True)],
    bedrock_service: Annotated[BedrockModelBase, MODEL_SERVICE_DEPENDS],
) -> ORJSONResponse:
    """
    Invoke Model API 用エンドポイント。
    ユーザーの入力に基づいてモデルを呼び出し、対話応答を返す。

    Args:
        bedrock_service (Annotated[BedrockModelBase, MODEL_SERVICE_DEPENDS]):
            モデルサービスのインスタンス。各種モデル固有の処理を提供する。
        user_input (Annotated[MessageList, Body, optional):
            ユーザーからの入力データ。

    Raises:
        HTTPException: 指定されたモデルが Converse API に対応していない、もしくは入力が無効な場合。

    Returns:
        ORJSONResponse: モデルからの応答を含むレスポンス。
    """
    if not isinstance(bedrock_service, ISupportsInvokeModel):
        raise HTTPException(status_code=400, detail="このモデルは対応してません")

    payload: BlobTypeDef = bedrock_service.generate_invoke_model_payload(user_input)

    response: str = await bedrock_service.invoke_model(payload)
    return ORJSONResponse(content=response)


@router.post("/invoke-model/stream")
async def invoke_model_stream(
    user_input: Annotated[MessageList, Body(..., description="ユーザーの入力", embed=True)],
    bedrock_service: Annotated[BedrockModelBase, MODEL_SERVICE_DEPENDS],
) -> StreamingResponse:
    """
    Invoke Model Stream API 用エンドポイント。
    ユーザーの入力に基づいてストリーミングでモデルの対話応答を返す。

    Args:
        bedrock_service (Annotated[BedrockModelBase, MODEL_SERVICE_DEPENDS]):
            モデルサービスのインスタンス。各種モデル固有の処理を提供する。
        user_input (Annotated[MessageList, Body, optional):
            ユーザーからの入力データ。

    Raises:
        HTTPException: 指定されたモデルが Converse API に対応していない、もしくは入力が無効な場合。

    Returns:
        StreamingResponse: ストリーミングで対話応答を含むレスポンス。
    """
    if not isinstance(bedrock_service, ISupportsInvokeModelStream):
        raise HTTPException(status_code=400, detail="このモデルは対応してません")

    payload: BlobTypeDef = bedrock_service.generate_invoke_model_stream_payload(user_input)

    stream_generator: AsyncGenerator[str, None] = bedrock_service.invoke_model_stream(payload)
    return StreamingResponse(stream_generator, media_type="text/plain")
