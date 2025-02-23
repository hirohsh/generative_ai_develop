"""
bedrock runtime client で使用する各種設定値を定義する。
"""

from app.types.bedrock_type_defs import ConfigTypeDef, LlamaConfigTypeDef

###################################################################
# Llama 3
###################################################################

LLAMA_MODEL_ID: str = "us.meta.llama3-3-70b-instruct-v1:0"

LLAMA_CONFIG: ConfigTypeDef[LlamaConfigTypeDef] = {
    "sdk": {
        "invoke": {"modelId": LLAMA_MODEL_ID, "contentType": "application/json", "body": ""},
        "invoke_stream": {"modelId": LLAMA_MODEL_ID, "contentType": "application/json", "body": ""},
        "converse": {
            "modelId": LLAMA_MODEL_ID,
            "inferenceConfig": {"maxTokens": 500, "temperature": 0.1, "topP": 0.9, "stopSequences": []},
        },
        "converse_stream": {
            "modelId": LLAMA_MODEL_ID,
            "inferenceConfig": {"maxTokens": 500, "temperature": 0.1, "topP": 0.9, "stopSequences": []},
        },
    },
    "model": {
        "invoke": {"prompt": "", "max_gen_len": 512, "temperature": 0.5, "top_p": 0.9},
        "invoke_stream": {"prompt": "", "max_gen_len": 512, "temperature": 0.5, "top_p": 0.9},
    },
}
