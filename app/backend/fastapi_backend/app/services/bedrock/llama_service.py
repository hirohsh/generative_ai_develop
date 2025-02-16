from __future__ import annotations

import json
from typing import TYPE_CHECKING, Any, TypedDict

from botocore.exceptions import ClientError
from fastapi import HTTPException
from fastapi.responses import ORJSONResponse

from app.interfaces.bedrock_interface import BedrockModelBase, ConfigTypeDef, ISupportsInvokeModel

if TYPE_CHECKING:
    from mypy_boto3_bedrock_runtime import BedrockRuntimeClient
    from mypy_boto3_bedrock_runtime.type_defs import BlobTypeDef, InvokeModelResponseTypeDef

    from app.routers.v1.bedrock_router import InvokeRequestTypeDef


# モデルに渡す設定の型
class LlamaConfigTypeDef(TypedDict):
    prompt: str
    temperature: float
    top_p: float
    max_gen_len: int


# モデルで使用する設定
LLAMA_CONFIG: ConfigTypeDef[LlamaConfigTypeDef] = {
    "sdk": {"modelId": "us.meta.llama3-3-70b-instruct-v1:0", "contentType": "application/json"},
    "model": {"prompt": "", "max_gen_len": 512, "temperature": 0.5, "top_p": 0.9},
}


class LlamaService(BedrockModelBase[LlamaConfigTypeDef], ISupportsInvokeModel):
    @classmethod
    def from_dependency(cls, client: BedrockRuntimeClient, config: ConfigTypeDef[LlamaConfigTypeDef]) -> LlamaService:
        """
        FastAPI の `Depends` で使用する依存性注入メソッド。
        依存性を注入したサービスのインスタンスを生成する。

        Args:
            client (BedrockRuntimeClient): bedrockのクライアント
            config (ConfigTypeDef[LlamaConfigTypeDef]): モデル設定

        Returns:
            LlamaService: サービスのインスタンス
        """
        return cls(client, config)

    def invoke_model(self, payload: BlobTypeDef) -> ORJSONResponse:
        """
        ペイロードを用いてモデルを呼び出す。

        Args:
            payload (BlobTypeDef): ペイロード

        Returns:
            ORJSONResponse: モデルからのレスポンス。
        """
        try:
            self.config["sdk"]["body"] = payload

            # モデルの呼び出し
            response: InvokeModelResponseTypeDef = self.client.invoke_model(**self.config["sdk"])

            # レスポンスの解析
            response_body: Any = json.loads(response["body"].read())
            generated_text: str = response_body["generation"]

            return ORJSONResponse(content=generated_text)
        except ClientError as e:
            print(f"エラーが発生しました: {e}")
            raise HTTPException(status_code=400, detail="無効な入力です") from e

    def generate_invoke_model_payload(self, user_input: InvokeRequestTypeDef) -> BlobTypeDef:
        """
        invoke_model用のペイロードを生成する。

        Args:
            user_input (BlobTypeDef): ユーザーからの入力

        Returns:
            BlobTypeDef: ペイロード
        """

        if not isinstance(user_input, str):
            raise HTTPException(status_code=400, detail="無効な入力です")

        # Llama 3.3 Instructモデル用のプロンプトフォーマット
        formatted_prompt: str = f"""
        <|begin_of_text|><|start_header_id|>user<|end_header_id|>
        {user_input}
        <|eot_id|>
        <|start_header_id|>assistant<|end_header_id|>
        """

        # リクエストペイロードの作成
        self.config["model"]["prompt"] = formatted_prompt
        request_payload: str = json.dumps(self.config["model"])

        return request_payload
