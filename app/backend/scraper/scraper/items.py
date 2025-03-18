# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy.item import Field, Item


class TechbizItem(Item):
    is_recruiting = Field()
    title = Field()
    remote = Field()
    price_min = Field()
    price_max = Field()
    places = Field()
    tags = Field()
    details = Field()
    required_skills = Field()
    welcome_skills = Field()
    meetings = Field()
    update_at = Field()
