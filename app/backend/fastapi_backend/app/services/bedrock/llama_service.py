from __future__ import annotations

import json
from typing import TYPE_CHECKING, Any, List

from botocore.exceptions import ClientError
from fastapi import HTTPException

from app.interfaces.bedrock_interface import (
    BedrockModelBase,
    ConfigTypeDef,
    SupportsConverseMixin,
    SupportsInvokeModelMixin,
)
from app.types.bedrock_type_defs import LlamaConfigTypeDef, LlamaInvokeRequestModelConfigTypeDef

if TYPE_CHECKING:
    from collections.abc import Sequence

    from mypy_boto3_bedrock_runtime import BedrockRuntimeClient
    from mypy_boto3_bedrock_runtime.type_defs import (
        BlobTypeDef,
        ContentBlockUnionTypeDef,
        ConverseRequestRequestTypeDef,
        ConverseResponseTypeDef,
        InvokeModelRequestRequestTypeDef,
        InvokeModelResponseTypeDef,
        MessageTypeDef,
        MessageUnionTypeDef,
    )

    from app.schemas.bedrock_schema import MessageList


class LlamaService(BedrockModelBase[LlamaConfigTypeDef], SupportsConverseMixin, SupportsInvokeModelMixin):
    """
    Llama3モデルに関する処理を提供するサービスクラス
    """

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

    def invoke_model(self, payload: BlobTypeDef) -> str:
        """
        ペイロードを用いてモデルを呼び出す。

        Args:
            payload (BlobTypeDef): ペイロード

        Returns:
            str: モデルからのレスポンス。
        """
        invoke_config: InvokeModelRequestRequestTypeDef = self.config["sdk"]["invoke"].copy()
        invoke_config["body"] = payload
        try:
            # モデルの呼び出し
            print(invoke_config)
            response: InvokeModelResponseTypeDef = self._invoke_model(self.client, invoke_config)

        except ClientError as e:
            print(f"エラーが発生しました: {e}")
            raise HTTPException(status_code=400, detail="無効な入力です") from e
        else:
            # レスポンスの解析
            response_body: Any = json.loads(response["body"].read())
            generated_text: str = response_body["generation"]

            return generated_text

    def generate_invoke_model_payload(self, message_list_schema: MessageList) -> BlobTypeDef:
        """
        invoke_model用のペイロードを生成する。

        Args:
            message_list_schema (MessageList): ユーザーからの入力

        Returns:
            BlobTypeDef: ペイロード
        """
        # いったん入力テキストをフォーマットするだけにする
        dumped_schema: dict[str, Any] = message_list_schema.model_dump()
        message: MessageTypeDef = dumped_schema["messages"][0]
        content: ContentBlockUnionTypeDef = message["content"][0]

        if "text" not in content or not content["text"].strip():
            raise HTTPException(status_code=400, detail="無効な入力です")

        # Llama 3.3 Instructモデル用のプロンプトフォーマット
        formatted_prompt: str = f"""
        <|begin_of_text|><|start_header_id|>user<|end_header_id|>
        {content["text"]}
        <|eot_id|>
        <|start_header_id|>assistant<|end_header_id|>
        """

        # リクエストペイロードの作成
        payload: LlamaInvokeRequestModelConfigTypeDef = self.config["model"]["invoke"].copy()
        payload["prompt"] = formatted_prompt
        request_payload: str = json.dumps(payload)

        return request_payload

    def converse(self, messages: Sequence[MessageUnionTypeDef]) -> str:
        """
        Converse API を使用して メッセージを送信する。

        Args:
            messages (Sequence[MessageUnionTypeDef]): ユーザーの会話履歴

        Returns:
            str: モデルからのレスポンス文字列。
        """
        converse_config: ConverseRequestRequestTypeDef = self.config["sdk"]["converse"].copy()
        converse_config["messages"] = messages
        try:
            # モデルの呼び出し
            print(converse_config)
            response: ConverseResponseTypeDef = self._converse(self.client, converse_config)
        except ClientError as e:
            print(f"エラーが発生しました: {e}")
            raise HTTPException(status_code=400, detail="無効な入力です") from e
        else:
            return response["output"]["message"]["content"][0]["text"]

    def generate_converse_messages(self, message_list_schema: MessageList) -> Sequence[MessageUnionTypeDef]:
        """
        Converse API に渡す会話履歴を作成する。

        Args:
            message_list_schema (MessageList): ユーザーの入力

        Returns:
            Sequence[MessageUnionTypeDef]: 会話履歴
        """
        # ここでDBなどから履歴を取得して入れてもいい
        # 今はいったんこのまま返す
        dumped_schema: dict[str, Any] = message_list_schema.model_dump(exclude_none=True)
        messages: List[MessageTypeDef] = dumped_schema["messages"]
        print(messages)
        return messages
