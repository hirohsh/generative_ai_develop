from typing import TYPE_CHECKING, Annotated

from fastapi import APIRouter, Body, HTTPException
from fastapi.responses import ORJSONResponse

from app.schemas.bedrock_schema import MessageList

if TYPE_CHECKING:
    from collections.abc import Sequence

    from mypy_boto3_bedrock_runtime.type_defs import BlobTypeDef, MessageUnionTypeDef

from app.dependencies.bedrock_dependencies import MODEL_SERVICE_DEPENDS
from app.interfaces.bedrock_interface import BedrockModelBase, ISupportsConverse, ISupportsInvokeModel

router = APIRouter(prefix="/bedrock", tags=["Bedrock"])


@router.post("/converse")
def converse(
    user_input: Annotated[MessageList, Body(..., description="ConverseAPI用のユーザー入力", embed=True)],
    bedrock_service: Annotated[BedrockModelBase, MODEL_SERVICE_DEPENDS],
) -> ORJSONResponse:
    if not isinstance(bedrock_service, ISupportsConverse):
        raise HTTPException(status_code=400, detail="このモデルは対応してません")

    converse_messages: Sequence[MessageUnionTypeDef] = bedrock_service.generate_converse_messages(user_input)
    reply_text: str = bedrock_service.converse(converse_messages)
    return ORJSONResponse(content=reply_text)


@router.post("/invoke-model")
def invoke_model(
    user_input: Annotated[MessageList, Body(..., description="ユーザーの入力", embed=True)],
    bedrock_service: Annotated[BedrockModelBase, MODEL_SERVICE_DEPENDS],
) -> ORJSONResponse:
    if not isinstance(bedrock_service, ISupportsInvokeModel):
        raise HTTPException(status_code=400, detail="このモデルは対応してません")

    payload: BlobTypeDef = bedrock_service.generate_invoke_model_payload(user_input)

    response: str = bedrock_service.invoke_model(payload)
    return ORJSONResponse(content=response)
