# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# useful for handling different item types with a single interface

import asyncio
import logging
import os

import scrapy
from scrapy.pipelines.images import ImagesPipeline

from .items import DjangoItemAssignment
from .settings import IMAGES_STORE

logger = logging.getLogger(__name__)


class PiracyCrawlPipeline(object):

    def process_item(self, item, spider):
        """处理爬虫传过来的数据
        将item进行json处理后, 保存到指定的文件中
        Arguments:
            item {dict} -- 数据的item对象
            spider {object} -- 产生item数据的爬虫

        Returns:
            dict -- Item对象
        """
        if item["title"] != "":
            logger.info("[写入数据库]:" + item["title"])
            # 写入数据库
            django_item = DjangoItemAssignment()
            django_item.do_assigned(item)
            asyncio.create_task(django_item.save())
        return item


class CoverPipeline(ImagesPipeline):
    FILE_PATH_ = None

    def get_media_requests(self, item, info):
        """ 爬取媒体文件 """
        # 请求图片数据
        if item["icon"]:
            logger.info("[开始爬取图片]:" + item["icon"])
            yield scrapy.Request(item["icon"])

    def file_path(self, request, response=None, info=None, *, item=None):
        """ 设置文件名称 """
        # 文件夹判断创建操作

        dir_name = os.path.join(item['source'], item["keyword"])
        total_path = os.path.join(IMAGES_STORE, dir_name)
        if not os.path.exists(total_path):
            os.makedirs(total_path)
        # 获取父类方法返回的图片名
        path = super().file_path(request, response, info)
        # 获取图片的16进制哈希名
        image_name = path.replace('full/', '')

        # 生成存储路径
        save_path = os.path.join(dir_name, image_name)
        logger.info(f"[图片存储路径]:{save_path}")
        item['icon'] = save_path
        return save_path

    def item_completed(self, results, item, info):
        """ 传递给下一个pipline """
        logger.info(f'[图片爬取完毕]:[{item["source"]}][{item["title"]}]')
        return item
