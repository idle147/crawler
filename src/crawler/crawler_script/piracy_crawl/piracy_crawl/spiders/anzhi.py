from urllib.parse import urlencode

import requests
import scrapy
from bs4 import BeautifulSoup

from .decorator import start_logged
from .spider_base import SpiderBase


class AnzhiSpider(SpiderBase):
    name = 'anzhi'
    # 允许请求的地址, 如果请求的域名不是这个, scrapy会自动过滤掉
    allowed_domains = ['www.anzhi.com']
    # 开始的url
    start_urls = ['http://www.anzhi.com/search.php?']
    # 标准URL
    base_url = "http://www.anzhi.com"

    def __init__(self, keyword, state_id, *args, **kwargs):
        super().__init__(keyword, state_id, *args, **kwargs)

    @start_logged
    def parse(self, response):
        params = {
            'keyword': self.keyword,
        }
        url = self.start_urls[0] + urlencode(params)
        self.logger.info("==== 开始anzhi游戏信息 ====")
        yield scrapy.Request(url, callback=self.parse_document)

    def parse_document(self, response):
        # BeautifulSoup捕获数据
        content = response.body
        soup = BeautifulSoup(content, "html.parser", from_encoding='utf-8')
        # 数据清洗
        try:
            infos = soup.select(
                "body > div.content > div.content_left > div.app_list.border_three > ul"
            )[0].find_all("li")
        except Exception:
            self.logger.critical(f"渠道[anzhi]关键词{self.keyword}查找错误。")
        else:
            for pos, info in enumerate(infos):
                # 访问info内的所有<li>标签信息爬取数据
                pos += 1
                app_icon = info.select(f"li:nth-child({pos}) > div.app_icon > a")[0]
                app_info = info.select(f"li:nth-child({pos}) > div.app_info")[0]

                yield self.item_opt(title=app_info.span.a.get_text(),
                                    link=self.base_url + app_info.span.a["href"],
                                    content=app_info.p.get_text(),
                                    icon=self._redirection(self.base_url + app_icon.img["src"]),
                                    source="安智渠道")

    def _redirection(self, url):
        """ 重定向设置 """
        # allow_redirects=False的意义为拒绝默认的301/302重定向
        # 从而可以通过html.headers[‘Location’]拿到重定向的URL。
        response = requests.get(url, verify=False, allow_redirects=False)
        return response.headers['Location']
