from collections.abc import Sequence
from typing import Protocol

from botocore.eventstream import EventStream
from botocore.response import StreamingBody
from mypy_boto3_bedrock_runtime.type_defs import BlobTypeDef, MessageTypeDef, MessageUnionTypeDef, ResponseStreamTypeDef


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


class ISupportsConverseStream(Protocol):
    """
    ConverseStream機能をサポートするモデル向けのプロトコル。

    継承するクラスは以下のメソッドを実装する必要がある:
    - converse_stream(self, messages: Sequence[MessageTypeDef]) -> str
    - generate_converse_stream_prompt(self, messages: Sequence[MessageTypeDef]) -> Sequence[MessageTypeDef] | None
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

    def generate_converse_stream_prompt(self, messages: Sequence[MessageTypeDef]) -> Sequence[MessageTypeDef] | None:
        """
        Converse API stream用のプロンプトを生成する。

        Args:
            messages (Sequence[MessageTypeDef]): テキスト

        Returns:
            Sequence[MessageTypeDef] | None: プロンプト
        """
        ...


class ISupportsInvokeModel(Protocol):
    """
    InvokeModel機能をサポートするモデル向けのプロトコル。

    継承するクラスは以下のメソッドを実装する必要がある:
    - invoke_model(self, payload: BlobTypeDef) -> StreamingBody
    - generate_invoke_model_payload(self, text: str) -> BlobTypeDef | None
    """

    def invoke_model(self, payload: BlobTypeDef) -> StreamingBody:
        """
        ペイロードを用いてモデルを呼び出す。

        Args:
            payload (BlobTypeDef): モデル呼び出しに必要なパラメータ

        Returns:
            StreamingBody: モデルからのレスポンス。
        """
        ...

    def generate_invoke_model_payload(self, text: str) -> BlobTypeDef | None:
        """
        invoke_model用のペイロードを生成する。

        Args:
            text (str): ユーザーからの入力

        Returns:
            BlobTypeDef | None: ペイロード
        """
        ...


class ISupportsInvokeModelStream(Protocol):
    """
    InvokeModelStream機能をサポートするモデル向けのプロトコル。

    継承するクラスは以下のメソッドを実装する必要がある:
    - invoke_model_stream(self, payload: BlobTypeDef) -> EventStream[ResponseStreamTypeDef]
    - generate_invoke_model_stream_payload(self, text: str) -> BlobTypeDef | None
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

    def generate_invoke_model_stream_payload(self, text: str) -> BlobTypeDef | None:
        """
        invoke_model_stream用のペイロードを生成する。

        Args:
            text (str): ユーザーからの入力

        Returns:
            BlobTypeDef | None: ペイロード
        """
        ...
