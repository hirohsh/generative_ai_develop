from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Generic, Protocol, TypedDict, TypeVar, runtime_checkable

from fastapi import UploadFile

if TYPE_CHECKING:
    from collections.abc import Sequence

    from botocore.eventstream import EventStream
    from fastapi.responses import ORJSONResponse
    from mypy_boto3_bedrock_runtime import BedrockRuntimeClient
    from mypy_boto3_bedrock_runtime.type_defs import (
        BlobTypeDef,
        InvokeModelRequestRequestTypeDef,
        MessageTypeDef,
        MessageUnionTypeDef,
        ResponseStreamTypeDef,
    )


# 型定義
T = TypeVar("T")


class ConfigTypeDef(TypedDict, Generic[T]):
    """
    bedrock用の設定を保持する`TypedDict`

    Attributes:
        sdk (InvokeModelRequestRequestTypeDef): SDKのメソッド呼び出し時に使用する設定。
        model (T): 各モデルに渡す設定。
    """

    sdk: InvokeModelRequestRequestTypeDef
    model: T


InvokeRequestTypeDef = str | bytes | UploadFile


class BedrockModelBase(ABC, Generic[T]):
    """
    bedrock モデルサービスの抽象基底クラス
    サービスクラスを作成する際、必ず継承すること。

    継承するクラスは以下のメソッドを実装する必要がある:
    - from_dependency(cls, client: BedrockRuntimeClient, config: ConfigTypeDef[T]) -> BedrockModelBase[T]:
    """

    def __init__(self, client: BedrockRuntimeClient, config: ConfigTypeDef[T]) -> None:
        self.client = client
        self.config = config

    @classmethod
    @abstractmethod
    def from_dependency(cls, client: BedrockRuntimeClient, config: ConfigTypeDef[T]) -> BedrockModelBase[T]:
        """
        FastAPI の `Depends` で使用する依存性注入メソッド。
        サブクラスで必ず実装し、依存性を注入したサービスのインスタンスを生成する。

        Args:
            client (BedrockRuntimeClient): bedrockのクライアント
            config (ConfigTypeDef[T]): モデル設定

        Returns:
            BedrockModelBase[T]: 設定を適用したサービスのインスタンス
        """
        ...


@runtime_checkable
class ISupportsConverse(Protocol):
    """
    Converse機能をサポートするモデル向けのプロトコル。

    継承するクラスは以下のメソッドを実装する必要がある:
    - converse(self, messages: Sequence[MessageUnionTypeDef]) -> str
    - generate_converse_prompt(self, messages: Sequence[MessageTypeDef]) -> Sequence[MessageUnionTypeDef] | None
    """

    def converse(self, messages: Sequence[MessageUnionTypeDef]) -> str:
        """Converse API を使用して テキストメッセージを送信する。

        Args:
            messages (Sequence[MessageUnionTypeDef]): プロンプト。

        Returns:
            str: モデルからのレスポンス文字列。
        """
        ...

    def generate_converse_prompt(self, messages: Sequence[MessageTypeDef]) -> Sequence[MessageUnionTypeDef] | None:
        """Converse API 用のプロンプトを生成する。

        Args:
            messages (Sequence[MessageTypeDef]): テキスト

        Returns:
            Sequence[MessageUnionTypeDef] | None: プロンプト
        """
        ...


@runtime_checkable
class ISupportsConverseStream(Protocol):
    """
    ConverseStream機能をサポートするモデル向けのプロトコル。

    継承するクラスは以下のメソッドを実装する必要がある:
    - converse_stream(self, messages: Sequence[MessageTypeDef]) -> str
    - generate_converse_stream_prompt(self, messages: Sequence[MessageTypeDef]) -> Sequence[MessageTypeDef]
    """

    def converse_stream(self, messages: Sequence[MessageTypeDef]) -> str:
        """
        Converse API streamを使用して テキストメッセージを送信する。

        Args:
            messages (Sequence[MessageTypeDef]): プロンプト。

        Returns:
            str: モデルからのレスポンス文字列。
        """
        ...

    def generate_converse_stream_prompt(self, messages: Sequence[MessageTypeDef]) -> Sequence[MessageTypeDef]:
        """
        Converse API stream用のプロンプトを生成する。

        Args:
            messages (Sequence[MessageTypeDef]): テキスト

        Returns:
            Sequence[MessageTypeDef]: プロンプト
        """
        ...


@runtime_checkable
class ISupportsInvokeModel(Protocol):
    """
    InvokeModel機能をサポートするモデル向けのプロトコル。

    継承するクラスは以下のメソッドを実装する必要がある:
    - invoke_model(self, payload: BlobTypeDef) -> StreamingBody
    - generate_invoke_model_payload(self, user_input (BlobTypeDef)) -> BlobTypeDef
    """

    def invoke_model(self, payload: BlobTypeDef) -> ORJSONResponse:
        """
        ペイロードを用いてモデルを呼び出す。

        Args:
            payload (BlobTypeDef): モデル呼び出しに必要なパラメータ

        Returns:
            ORJSONResponse: モデルからのレスポンス。
        """
        ...

    def generate_invoke_model_payload(self, user_input: InvokeRequestTypeDef) -> BlobTypeDef:
        """
        invoke_model用のペイロードを生成する。

        Args:
            user_input (BlobTypeDef): ユーザーからの入力

        Returns:
            BlobTypeDef: ペイロード
        """
        ...


@runtime_checkable
class ISupportsInvokeModelStream(Protocol):
    """
    InvokeModelStream機能をサポートするモデル向けのプロトコル。

    継承するクラスは以下のメソッドを実装する必要がある:
    - invoke_model_stream(self, payload: BlobTypeDef) -> EventStream[ResponseStreamTypeDef]
    - generate_invoke_model_stream_payload(self, user_input (BlobTypeDef)) -> BlobTypeDef
    """

    def invoke_model_stream(self, payload: BlobTypeDef) -> EventStream[ResponseStreamTypeDef]:
        """
        ペイロードを用いてモデルを呼び出す。

        Args:
            payload (BlobTypeDef): モデル呼び出しに必要なパラメータ

        Returns:
            EventStream[ResponseStreamTypeDef]: モデルからのレスポンス。
        """
        ...

    def generate_invoke_model_stream_payload(self, user_input: BlobTypeDef) -> BlobTypeDef:
        """
        invoke_model_stream用のペイロードを生成する。

        Args:
            user_input (BlobTypeDef): ユーザーからの入力

        Returns:
            BlobTypeDef: ペイロード
        """
        ...
