from typing import Any, Dict, List

from mypy_boto3_bedrock_runtime.literals import (
    ConversationRoleType,
    DocumentFormatType,
    GuardrailConverseContentQualifierType,
    GuardrailConverseImageFormatType,
    ImageFormatType,
    ToolResultStatusType,
    VideoFormatType,
)
from mypy_boto3_bedrock_runtime.type_defs import BlobTypeDef
from pydantic import BaseModel, ConfigDict, Field


###############################################################################################################################
# SDK MessageTypeDefのモデル定義
###############################################################################################################################
class S3Location(BaseModel):
    uri: str
    bucketOwner: str | None = None  # noqa: N815


# ── ソース型 ──


# 画像ソース
class ImageSource(BaseModel):
    bytes: BlobTypeDef | None
    model_config = ConfigDict(arbitrary_types_allowed=True)


class ImageSourceOutput(BaseModel):
    bytes: bytes | None


ImageSourceUnion = ImageSource | ImageSourceOutput


# 文書ソース
class DocumentSource(BaseModel):
    bytes: BlobTypeDef | None
    model_config = ConfigDict(arbitrary_types_allowed=True)


class DocumentSourceOutput(BaseModel):
    bytes: bytes | None


DocumentSourceUnion = DocumentSource | DocumentSourceOutput


# 動画ソース
class VideoSource(BaseModel):
    bytes: BlobTypeDef | None = None
    s3Location: S3Location | None = None  # noqa: N815
    model_config = ConfigDict(arbitrary_types_allowed=True)


class VideoSourceOutput(BaseModel):
    video_bytes: bytes | None = Field(default=None, alias="bytes")
    s3Location: S3Location | None = None  # noqa: N815


VideoSourceUnion = VideoSource | VideoSourceOutput

# ── ブロック型 ──


# 画像ブロック
class ImageBlock(BaseModel):
    format: ImageFormatType
    source: ImageSourceUnion


class ImageBlockOutput(BaseModel):
    format: ImageFormatType
    source: ImageSourceOutput


ImageBlockUnion = ImageBlock | ImageBlockOutput


# 文書ブロック
class DocumentBlock(BaseModel):
    format: DocumentFormatType
    name: str
    source: DocumentSourceUnion


class DocumentBlockOutput(BaseModel):
    format: DocumentFormatType
    name: str
    source: DocumentSourceOutput


DocumentBlockUnion = DocumentBlock | DocumentBlockOutput


# 動画ブロック
class VideoBlock(BaseModel):
    format: VideoFormatType
    source: VideoSourceUnion


class VideoBlockOutput(BaseModel):
    format: VideoFormatType
    source: VideoSourceOutput


VideoBlockUnion = VideoBlock | VideoBlockOutput


# ツール利用ブロック
class ToolUseBlock(BaseModel):
    toolUseId: str  # noqa: N815
    name: str
    input: Dict[str, Any]


class ToolUseBlockOutput(BaseModel):
    toolUseId: str  # noqa: N815
    name: str
    input: Dict[str, Any]


ToolUseBlockUnion = ToolUseBlock | ToolUseBlockOutput


# ツール結果コンテンツブロック
class ToolResultContentBlock(BaseModel):
    json_data: Dict[str, Any] | None = Field(default=None, alias="json")
    text: str | None = None
    image: ImageBlockUnion | None = None
    document: DocumentBlockUnion | None = None
    video: VideoBlockUnion | None = None


class ToolResultContentBlockOutput(BaseModel):
    json_data: Dict[str, Any] | None = Field(default=None, alias="json")
    text: str | None = None
    image: ImageBlockOutput | None = None
    document: DocumentBlockOutput | None = None
    video: VideoBlockOutput | None = None


ToolResultContentBlockUnion = ToolResultContentBlock | ToolResultContentBlockOutput


# ツール結果ブロック
class ToolResultBlock(BaseModel):
    toolUseId: str  # noqa: N815
    content: List[ToolResultContentBlockUnion]
    status: ToolResultStatusType | None = None


class ToolResultBlockOutput(BaseModel):
    toolUseId: str  # noqa: N815
    content: List[ToolResultContentBlockOutput]
    status: ToolResultStatusType | None = None


ToolResultBlockUnion = ToolResultBlock | ToolResultBlockOutput

# ── ガードレール会話ブロック ──


# ガードレール会話テキストブロック
class GuardrailConverseTextBlock(BaseModel):
    text: str
    qualifiers: List[GuardrailConverseContentQualifierType] | None = None


class GuardrailConverseTextBlockOutput(BaseModel):
    text: str
    qualifiers: List[GuardrailConverseContentQualifierType] | None = None


GuardrailConverseTextBlockUnion = GuardrailConverseTextBlock | GuardrailConverseTextBlockOutput


# ガードレール会話画像ソース
class GuardrailConverseImageSource(BaseModel):
    bytes: BlobTypeDef | None
    model_config = ConfigDict(arbitrary_types_allowed=True)


class GuardrailConverseImageSourceOutput(BaseModel):
    bytes: bytes | None


# ガードレール会話画像ブロック
class GuardrailConverseImageBlock(BaseModel):
    format: GuardrailConverseImageFormatType
    source: GuardrailConverseImageSource


class GuardrailConverseImageBlockOutput(BaseModel):
    format: GuardrailConverseImageFormatType
    source: GuardrailConverseImageSourceOutput


GuardrailConverseImageBlockUnion = GuardrailConverseImageBlock | GuardrailConverseImageBlockOutput


# ガードレール会話コンテンツブロック
class GuardrailConverseContentBlock(BaseModel):
    text: GuardrailConverseTextBlockUnion | None = None
    image: GuardrailConverseImageBlockUnion | None = None


class GuardrailConverseContentBlockOutput(BaseModel):
    text: GuardrailConverseTextBlockOutput | None = None
    image: GuardrailConverseImageBlockOutput | None = None


GuardrailConverseContentBlockUnion = GuardrailConverseContentBlock | GuardrailConverseContentBlockOutput

# ── ContentBlock 型 ──


# 通常のコンテンツブロック
class ContentBlock(BaseModel):
    text: str | None = None
    image: ImageBlockUnion | None = None
    document: DocumentBlockUnion | None = None
    video: VideoBlockUnion | None = None
    toolUse: ToolUseBlockUnion | None = None  # noqa: N815
    toolResult: ToolResultBlockUnion | None = None  # noqa: N815
    guardContent: GuardrailConverseContentBlockUnion | None = None  # noqa: N815


# 出力用コンテンツブロック
class ContentBlockOutput(BaseModel):
    text: str | None = None
    image: ImageBlockOutput | None = None
    document: DocumentBlockOutput | None = None
    video: VideoBlockOutput | None = None
    toolUse: ToolUseBlockOutput | None = None  # noqa: N815
    toolResult: ToolResultBlockOutput | None = None  # noqa: N815
    guardContent: GuardrailConverseContentBlockOutput | None = None  # noqa: N815


ContentBlockUnion = ContentBlock | ContentBlockOutput


class Message(BaseModel):
    role: ConversationRoleType
    content: List[ContentBlockUnion]


class MessageList(BaseModel):
    messages: List[Message]


# ── Forward Ref の更新 ──
MessageList.model_rebuild()
