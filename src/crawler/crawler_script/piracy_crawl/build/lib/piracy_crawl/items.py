# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from channels.db import database_sync_to_async
from inspection.models import InfoModel
from scrapy_djangoitem import DjangoItem


class InfoItem(scrapy.Item):
    """ 引入了djangoItem """
    keyword = scrapy.Field()
    source = scrapy.Field()
    owner = scrapy.Field()
    source_state = scrapy.Field()
    title = scrapy.Field()
    link = scrapy.Field()
    content = scrapy.Field()
    icon = scrapy.Field()


class DjangoModelItem(DjangoItem):
    """ 引入了djangoItem """
    django_model = InfoModel


class DjangoItemAssignment():
    """ 借助DjangoItem写入数据库 """

    def __init__(self) -> None:
        self.django_item = DjangoModelItem()

    def do_assigned(self, item: InfoItem):
        self.django_item["title"] = item["title"]
        self.django_item["link"] = item["link"]
        self.django_item["content"] = item["content"]
        self.django_item["icon"] = item["icon"]
        self.django_item["source_state"] = item["source_state"]
        self.django_item["owner"] = item["owner"]

    async def save(self):
        await database_sync_to_async(self.django_item.save)()
