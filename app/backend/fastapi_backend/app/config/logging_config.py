import logging
from pathlib import Path
from typing import Any


class ModuleFilter(logging.Filter):
    """特定のモジュールのプレフィックスでフィルタリング"""

    def __init__(self, prefix: str | tuple[str, ...]) -> None:
        super().__init__()
        self.prefix = prefix

    def filter(self, record: logging.LogRecord) -> bool:
        return record.name.startswith(self.prefix)


# ログフォルダ名
LOG_DIR_NAME: Path = Path("logs")

LOGGING_CONFIG: dict[str, Any] = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s - PID:%(process)d - %(threadName)s - [%(name)s] - %(levelname)s : %(message)s",
        },
        "uvicorn-error": {
            "format": "%(asctime)s - PID:%(process)d - %(threadName)s - [uvicorn] - %(levelname)s : %(message)s",
        },
        "uvicorn-access": {
            "format": "%(asctime)s - PID:%(process)d - %(threadName)s - [%(name)s] - %(levelname)s - %(client_addr)s : '%(request_line)s' %(status_code)s",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "default",
            "stream": "ext://sys.stdout",
        },
        "file": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "level": "DEBUG",
            "formatter": "default",
            "filename": Path.joinpath(LOG_DIR_NAME, "generative_ai_backend.log"),
            "when": "midnight",  # 毎日0時に新ファイルへ切り替え
            "interval": 1,  # 1日ごと("midnight" と組み合わせ)
            "backupCount": 14,  # 14日分のログを保持
            "encoding": "utf-8",
        },
        "uvicorn-error": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "level": "INFO",
            "formatter": "uvicorn-error",
            "filename": Path.joinpath(LOG_DIR_NAME, "generative_ai_backend.log"),
            "when": "midnight",  # 毎日0時に新ファイルへ切り替え
            "interval": 1,  # 1日ごと("midnight" と組み合わせ)
            "backupCount": 14,  # 14日分のログを保持
            "encoding": "utf-8",
        },
        "uvicorn-access": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "level": "INFO",
            "formatter": "uvicorn-access",
            "filename": Path.joinpath(LOG_DIR_NAME, "generative_ai_backend.log"),
            "when": "midnight",  # 毎日0時に新ファイルへ切り替え
            "interval": 1,  # 1日ごと("midnight" と組み合わせ)
            "backupCount": 14,  # 14日分のログを保持
            "encoding": "utf-8",
        },
    },
    "loggers": {
        "app": {
            "handlers": ["console", "file"],
            "level": "DEBUG",
            "propagate": False,
        },
        "uvicorn.access": {
            "handlers": ["console", "uvicorn-access"],
            "level": "INFO",
            "propagate": False,
        },
        "uvicorn.error": {
            "handlers": ["console", "uvicorn-error"],
            "level": "INFO",
            "propagate": False,
        },
    },
}
