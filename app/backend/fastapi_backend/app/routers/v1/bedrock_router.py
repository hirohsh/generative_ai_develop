from typing import TYPE_CHECKING

from fastapi import APIRouter, HTTPException
from fastapi.responses import ORJSONResponse

from app.services.bedrock import MODEL_SERVICE_DEPENDS, USER_INPUT_QUERY

if TYPE_CHECKING:
    from mypy_boto3_bedrock_runtime.type_defs import BlobTypeDef

from app.interfaces.bedrock_interface import BedrockModelBase, InvokeRequestTypeDef, ISupportsInvokeModel

router = APIRouter(prefix="/bedrock", tags=["Bedrock"])


@router.post("/invoke-model")
def invoke_model(
    user_input: InvokeRequestTypeDef = USER_INPUT_QUERY, bedrock_service: BedrockModelBase = MODEL_SERVICE_DEPENDS
) -> ORJSONResponse:
    if not isinstance(bedrock_service, ISupportsInvokeModel):
        raise HTTPException(status_code=400, detail="このモデルは対応してません")

    payload: BlobTypeDef = bedrock_service.generate_invoke_model_payload(user_input)

    return bedrock_service.invoke_model(payload)
