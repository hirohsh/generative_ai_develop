import json
import logging
import sys
from typing import Any, Dict

import scrapy
from aws_lambda_typing.context import Context
from scrapy.crawler import CrawlerProcess
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
from twisted.internet.asyncioreactor import install

from scraper.mappings import SITE_SPIDER_MAPPING, TECHBIZ_TARGET_MAPPING, Sites, TechbizMenuSkills

install()  # type: ignore  # noqa: PGH003

# Scrapyの既定のログ設定を無効化
configure_logging(install_root_handler=False)

# 既存のハンドラーを全て削除
for handle in logging.root.handlers[:]:
    logging.root.removeHandler(handle)

# ログの設定
logging.basicConfig(
    format="%(asctime)s - PID:%(process)d - %(threadName)s - [%(name)s] - %(levelname)s : %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.ERROR,
    stream=sys.stdout,
)

logger = logging.getLogger()


def get_spider(site_name: str) -> type[scrapy.Spider] | None:
    """
    サイト名(文字列)から対応するspiderを取得する。
    存在しないサイト名の場合は None を返す。
    """
    try:
        site_enum: Sites = Sites(site_name)
        return SITE_SPIDER_MAPPING.get(site_enum)
    except ValueError:
        return None  # 無効なサイト名が渡された場合は None を返す


def get_skill_code(skill_name: str) -> str | None:
    """
    スキル名(文字列)から対応するエンドポイントコードを取得する。
    存在しないスキル名の場合は None を返す。
    """
    try:
        skill_enum: TechbizMenuSkills = TechbizMenuSkills(skill_name)
        return TECHBIZ_TARGET_MAPPING.get(skill_enum)
    except ValueError:
        return None  # 無効なスキル名が渡された場合は None を返す


def handler(event: Dict[str, Any], context: Context) -> dict[str, Any]:  # noqa: ARG001
    """
    SQS から受け取ったメッセージを処理し、Scrapy を実行する Lambda ハンドラー
    """
    records: list[Dict[str, Any]] = event.get("Records", [])

    if not records:
        logger.warning("No records found in event")
        return {"statusCode": 400, "body": "No records found"}

    settings = get_project_settings()
    process = CrawlerProcess(settings)

    for record in records:
        try:
            message_body = json.loads(record.get("body", "{}"))  # メッセージのボディを取得
            logger.info("Received SQS message: %s", message_body)

            # Spider取得
            spider: type[scrapy.Spider] | None = get_spider(message_body.get("site_name", ""))
            # target取得
            target: str | None = get_skill_code(message_body.get("skill_name", ""))

            if spider is None or target is None:
                logger.warning("Invalid site_name or skill_name in message: %s", message_body)
                continue  # 無効なメッセージはスキップ

            # Scrapy の実行
            process.crawl(spider, target=target)

        except json.JSONDecodeError:
            logger.exception("Invalid JSON format in message body: %s", record.get("body"))
            continue  # JSON が無効な場合はスキップ

    # Scrapyを開始
    process.start(stop_after_crawl=True)

    return {"statusCode": 200, "body": "Scrapy crawling finished!"}
