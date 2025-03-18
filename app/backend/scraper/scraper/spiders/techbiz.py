import json
import logging
from typing import Any, Generator, List

import scrapy
from scrapy.http import Response

from scraper.items import TechbizItem


class TechbizSpider(scrapy.Spider):
    """
    techbiz用スパイダー
    エンドポイントは動的に変更する
    """

    name: str = "techbiz"
    allowed_domains: list[str] = ["techbiz.com"]  # noqa: RUF012
    base_url: str = "https://techbiz.com/project/pc/search/"

    custom_settings = {  # noqa: RUF012
        "ITEM_PIPELINES": {
            "scraper.pipelines.S3SavePipeline": 1,
        }
    }

    def __init__(self, target: str = "skill-6", limit: int = 50, **kwargs: Any) -> None:  # noqa: ANN401
        logging.getLogger("scrapy").setLevel(logging.ERROR)
        super().__init__(**kwargs)
        self.start_urls = [self.base_url + target]
        self.target = target
        self.skill_id = target.split("-")[-1]
        self.limit = limit

    def start_requests(self) -> Generator[scrapy.Request, Any]:
        """
        最初に実行される処理
        ページ数を確認するために１回実行する
        """
        yield scrapy.Request(url=self.start_urls[0], callback=self.parse_start)

    def parse_start(self, response: Response) -> Generator[scrapy.Request, Any]:
        """
        start_requestsのリクエスト結果を解析する
        取得したページ数分リクエストを投げる
        """
        # ページャーのボタン数を取得
        page_list: List[str] = response.css('nav[aria-label="ページ選択"] ul li button::text').getall()
        pager_min_count: int = 3
        # データがない場合、「前へ」「次へ」ボタンの2つだけになるので処理を行わない
        if len(page_list) >= pager_min_count:
            page_count: int = int(page_list[-2])  # ページの最大数を取得

            for page in range(1, page_count + 1):
                offset_count: int = page * self.limit - self.limit
                page_url = f"https://search-api.techbiz.com/api/project?orderType=new&skills={self.skill_id}&isOnlyRecruiting=false&tagIds={self.skill_id}&limit={self.limit}&offset={offset_count}"
                yield scrapy.Request(url=page_url, callback=self.parse_page)

    def parse_page(self, response: Response) -> Generator[TechbizItem]:
        """
        parse_startのリクエスト結果を解析する
        jsonデータが渡ってくるので、必要な情報を抜き出す
        """
        data = json.loads(response.text)
        for item in data["projects"]:
            techbiz_item: TechbizItem = TechbizItem()
            techbiz_item["is_recruiting"] = item["isRecruiting"]
            techbiz_item["title"] = item["title"]
            techbiz_item["remote"] = [condition["name"] for condition in item["preferredConditions"]]
            techbiz_item["price_min"] = item["priceMin"]
            techbiz_item["price_max"] = item["priceMax"]
            techbiz_item["places"] = [{"name": location["name"], "prefecture": location["prefecture"]["name"]} for location in item["locations"]]
            techbiz_item["tags"] = [tag["name"] for tag in item["tags"]]
            techbiz_item["details"] = item["detail"]
            techbiz_item["required_skills"] = item["requiredSkillDescription"]
            techbiz_item["welcome_skills"] = item["preferredSkillDescription"]
            techbiz_item["meetings"] = item["negotiationCount"]
            techbiz_item["update_at"] = item["updatedAt"]
            yield techbiz_item
