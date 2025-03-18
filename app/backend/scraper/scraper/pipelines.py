# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import json
import logging
import os
from typing import Any

import boto3
import scrapy
from dotenv import load_dotenv
from scrapy.exceptions import DropItem

from scraper.items import TechbizItem

# if TYPE_CHECKING:

load_dotenv()
boto3.set_stream_logger("", logging.ERROR)


class S3SavePipeline:
    """
    s3操作用パイプライン
    """

    def __init__(self) -> None:
        self.bucket_name = os.getenv("AWS_S3_BUCKET")
        self.s3_client = boto3.client("s3")
        self.items: list[dict[str, Any]] = []

    def delete_specific_file(self, bucket_name: str, file_name: str, spider: scrapy.Spider) -> None:
        """
        指定されたファイルを S3 から削除する
        """
        try:
            self.s3_client.head_object(Bucket=bucket_name, Key=file_name)  # ファイルが存在するか確認
            self.s3_client.delete_object(Bucket=bucket_name, Key=file_name)
            spider.logger.info("Deleted specific file from S3: s3://%s/%s", self.bucket_name, file_name)
        except self.s3_client.exceptions.ClientError as e:
            if e.response["Error"]["Code"] == "404":
                spider.logger.info("File not found, skipping deletion: s3://%s/%s", self.bucket_name, file_name)
            else:
                raise

    def process_item(self, item: TechbizItem, spider: scrapy.Spider) -> TechbizItem:  # noqa: ARG002
        """
        一時的にアイテムをリストに保存する
        """
        self.items.append(dict(item))
        return item

    def close_spider(self, spider: scrapy.Spider) -> None:
        """
        Scrapy が終了するときに S3 にアップロード
        """
        if not self.items:
            error_message = "No items scraped, skipping upload to S3"
            raise DropItem(error_message)

        if self.bucket_name is None:
            error_message = "AWS_S3_BUCKET 環境変数が設定されていません。"
            raise ValueError(error_message)

        target: str = spider.start_urls[0].split("/")[-1]
        file_name = f"{target}.json"

        # JSON データを作成
        json_data = json.dumps(self.items, ensure_ascii=False, indent=2)

        # S3から既存のファイルを削除
        self.delete_specific_file(self.bucket_name, file_name, spider)

        # S3 にアップロード
        self.s3_client.put_object(Bucket=self.bucket_name, Key=file_name, Body=json_data.encode("utf-8"), ContentType="application/json")

        spider.logger.info("Uploaded data to S3: s3://%s/%s", self.bucket_name, file_name)
