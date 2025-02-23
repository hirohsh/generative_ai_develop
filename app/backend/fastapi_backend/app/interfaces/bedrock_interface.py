"""
Bedrock モデル向けのプロトコルと抽象クラスを定義する。
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, AsyncGenerator, Generic, Protocol, runtime_checkable

from app.types.bedrock_type_defs import ConfigTypeDef, T

if TYPE_CHECKING:
    from collections.abc import Sequence

    from mypy_boto3_bedrock_runtime import BedrockRuntimeClient
    from mypy_boto3_bedrock_runtime.type_defs import (
        BlobTypeDef,
        ConverseRequestRequestTypeDef,
        ConverseResponseTypeDef,
        ConverseStreamRequestRequestTypeDef,
        ConverseStreamResponseTypeDef,
        InvokeModelRequestRequestTypeDef,
        InvokeModelResponseTypeDef,
        InvokeModelWithResponseStreamRequestRequestTypeDef,
        InvokeModelWithResponseStreamResponseTypeDef,
        MessageTypeDef,
        MessageUnionTypeDef,
    )

    from app.schemas.bedrock_schema import MessageList

####################################################################################################
# プロトコル定義
####################################################################################################


@runtime_checkable
class ISupportsConverse(Protocol):
    """
    Converse機能をサポートするモデル向けのプロトコル。

    継承するクラスは以下のメソッドを実装する必要がある:
    - converse
    - generate_converse_messages
    """

    async def converse(self, messages: Sequence[MessageUnionTypeDef]) -> str:
        """
        Converse API を使用して メッセージを送信する。

        Args:
            messages (Sequence[MessageUnionTypeDef]): ユーザーの会話履歴

        Returns:
            str: モデルからのレスポンス文字列。
        """
        ...

    def generate_converse_messages(self, message_list_schema: MessageList) -> Sequence[MessageUnionTypeDef]:
        """
        Converse API に渡す会話履歴を作成する。

        Args:
            message_list_schema (MessageList): ユーザーの入力

        Returns:
            Sequence[MessageUnionTypeDef]: 会話履歴
        """
        ...


@runtime_checkable
class ISupportsConverseStream(Protocol):
    """
    ConverseStream機能をサポートするモデル向けのプロトコル。

    継承するクラスは以下のメソッドを実装する必要がある:
    - converse_stream
    - generate_converse_stream_messages
    """

    def converse_stream(self, messages: Sequence[MessageTypeDef]) -> AsyncGenerator[str, None]:
        """
        Converse Stream API を使用して メッセージを送信する。

        Args:
            messages (Sequence[MessageUnionTypeDef]): ユーザーの会話履歴

        Yields:
            str: 各チャンクの部分的なレスポンス
        """
        ...

    def generate_converse_stream_messages(self, message_list_schema: MessageList) -> Sequence[MessageTypeDef]:
        """
        Converse Stream API に渡す会話履歴を作成する。

        Args:
            message_list_schema (MessageList): ユーザーの入力

        Returns:
            Sequence[MessageUnionTypeDef]: 会話履歴
        """
        ...


@runtime_checkable
class ISupportsInvokeModel(Protocol):
    """
    InvokeModel機能をサポートするモデル向けのプロトコル。

    継承するクラスは以下のメソッドを実装する必要がある:
    - invoke_model
    - generate_invoke_model_payload
    """

    async def invoke_model(self, payload: BlobTypeDef) -> str:
        """
        ペイロードを用いてモデルを呼び出す。

        Args:
            payload (BlobTypeDef): ペイロード

        Returns:
            str: モデルからのレスポンス。
        """
        ...

    def generate_invoke_model_payload(self, message_list_schema: MessageList) -> BlobTypeDef:
        """
        invoke_model用のペイロードを生成する。

        Args:
            message_list_schema (MessageList): ユーザーからの入力

        Returns:
            BlobTypeDef: ペイロード
        """
        ...


@runtime_checkable
class ISupportsInvokeModelStream(Protocol):
    """
    InvokeModelStream機能をサポートするモデル向けのプロトコル。

    継承するクラスは以下のメソッドを実装する必要がある:
    - invoke_model_stream
    - generate_invoke_model_stream_payload
    """

    def invoke_model_stream(self, payload: BlobTypeDef) -> AsyncGenerator[str, None]:
        """
        ペイロードを用いてモデルを呼び出す。

        Args:
            payload (BlobTypeDef): ペイロード

        Yields:
            str: 各チャンクの部分的なレスポンス
        """
        ...

    def generate_invoke_model_stream_payload(self, message_list_schema: MessageList) -> BlobTypeDef:
        """
        invoke_model_stream用のペイロードを生成する。

        Args:
            message_list_schema (MessageList): ユーザーからの入力

        Returns:
            BlobTypeDef: ペイロード
        """
        ...


#####################################################################################################
# 抽象クラス定義
#####################################################################################################


class BedrockModelBase(ABC, Generic[T]):
    """
    bedrock モデルサービスの抽象基底クラス
    サービスクラスを作成する際、必ず継承すること。

    継承するクラスは以下のメソッドを実装する必要がある:
    - from_dependency
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


class SupportsConverseMixin(ABC, ISupportsConverse):
    """
    converse APIの機能を提供するMixin
    converse APIをサポートしているモデルのサービスクラスに継承すること。

    継承するクラスは以下のメソッドを実装する必要がある:
    - converse
    - generate_converse_messages
    """

    @staticmethod
    def _converse(client: BedrockRuntimeClient, request_args: ConverseRequestRequestTypeDef) -> ConverseResponseTypeDef:
        """
        Converse API を使用して メッセージを送信する。
        このメソッドは直接使用せず、継承先でラップして使用すること。

        Args:
            client (BedrockRuntimeClient): bedrockランタイムクライアント
            requestArgs (ConverseRequestRequestTypeDef): converseメソッドの引数に渡すパラメータ

        Returns:
            ConverseResponseTypeDef: モデルからのレスポンス
        """

        response: ConverseResponseTypeDef = client.converse(**request_args)

        return response

    @abstractmethod
    async def converse(self, messages: Sequence[MessageUnionTypeDef]) -> str:
        """
        Converse API を使用して メッセージを送信する。
        _converseメソッドを内部で使用すること。
        """

    @abstractmethod
    def generate_converse_messages(self, message_list_schema: MessageList) -> Sequence[MessageUnionTypeDef]:
        """
        Converse API に渡す会話履歴を作成する。
        """
        ...


class SupportsConverseStreamMixin(ABC, ISupportsConverseStream):
    """
    converse stream APIの機能を提供するMixin
    converse stream APIをサポートしているモデルのサービスクラスに継承すること。

    継承するクラスは以下のメソッドを実装する必要がある:
    - converse_stream
    - generate_converse_stream_messages
    """

    @staticmethod
    def _converse_stream(
        client: BedrockRuntimeClient, request_args: ConverseStreamRequestRequestTypeDef
    ) -> ConverseStreamResponseTypeDef:
        """
        Converse Stream API を使用して メッセージを送信する。
        このメソッドは直接使用せず、継承先でラップして使用すること。

        Args:
            client (BedrockRuntimeClient): bedrockランタイムクライアント
            requestArgs (ConverseStreamRequestRequestTypeDef): converse_streamメソッドに渡すパラメータ

        Returns:
            ConverseStreamRequestRequestTypeDef: モデルからのレスポンス
        """
        response: ConverseStreamResponseTypeDef = client.converse_stream(**request_args)
        return response

    @abstractmethod
    def converse_stream(self, messages: Sequence[MessageTypeDef]) -> AsyncGenerator[str, None]:
        """
        Converse Stream API を使用して メッセージを送信する。
        __converse_streamメソッドを内部で使用すること。
        """
        ...

    @abstractmethod
    def generate_converse_stream_messages(self, message_list_schema: MessageList) -> Sequence[MessageTypeDef]:
        """
        Converse Stream API に渡す会話履歴を作成する。
        """
        ...


class SupportsInvokeModelMixin(ABC, ISupportsInvokeModel):
    """
    inveke modelの機能を提供するMixin
    inveke modelをサポートしているモデルのサービスクラスに継承すること。

    継承するクラスは以下のメソッドを実装する必要がある:
    - invoke_model
    - generate_invoke_model_payload
    """

    @staticmethod
    def _invoke_model(client: BedrockRuntimeClient, request_args: InvokeModelRequestRequestTypeDef) -> InvokeModelResponseTypeDef:
        """
        ペイロードを用いてモデルを呼び出す。
        このメソッドは直接使用せず、継承先でラップして使用すること。

        Args:
            client (BedrockRuntimeClient): bedrockランタイムクライアント
            request_args (InvokeModelRequestRequestTypeDef): invoke_modelメソッドの引数に渡すパラメータ

        Returns:
            InvokeModelResponseTypeDef: モデルからのレスポンス
        """
        response: InvokeModelResponseTypeDef = client.invoke_model(**request_args)
        return response

    @abstractmethod
    async def invoke_model(self, payload: BlobTypeDef) -> str:
        """
        ペイロードを用いてモデルを呼び出す。
        _invoke_modelメソッドを内部で使用すること。
        """
        ...

    @abstractmethod
    def generate_invoke_model_payload(self, message_list_schema: MessageList) -> BlobTypeDef:
        """
        invoke_model用のペイロードを生成する。
        """
        ...


class SupportsInvokeModelStreamMixin(ABC, ISupportsInvokeModelStream):
    """
    inveke model streamの機能を提供するMixin
    inveke model streamの機能を提供するMixinをサポートしているモデルのサービスクラスに継承すること。

    継承するクラスは以下のメソッドを実装する必要がある:
    - invoke_model_stream
    - generate_invoke_model_stream_payload
    """

    @staticmethod
    def _invoke_model_stream(
        client: BedrockRuntimeClient, request_args: InvokeModelWithResponseStreamRequestRequestTypeDef
    ) -> InvokeModelWithResponseStreamResponseTypeDef:
        """
        ペイロードを用いてモデルを呼び出す。
        このメソッドは直接使用せず、継承先でラップして使用すること。

        Args:
            client (BedrockRuntimeClient): bedrockランタイムクライアント
            request_args (InvokeModelWithResponseStreamRequestRequestTypeDef):
                invoke_model_with_response_streamメソッドの引数に渡すパラメータ

        Returns:
            InvokeModelWithResponseStreamResponseTypeDef: モデルからのレスポンス
        """
        response: InvokeModelWithResponseStreamResponseTypeDef = client.invoke_model_with_response_stream(**request_args)
        return response

    @abstractmethod
    def invoke_model_stream(self, payload: BlobTypeDef) -> AsyncGenerator[str, None]:
        """
        ペイロードを用いてモデルを呼び出す。
        _invoke_model_streamメソッドを内部で使用すること。
        """
        ...

    @abstractmethod
    def generate_invoke_model_stream_payload(self, message_list_schema: MessageList) -> BlobTypeDef:
        """
        invoke_model_stream用のペイロードを生成する。
        """
        ...
