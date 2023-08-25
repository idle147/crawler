from urllib.parse import urlencode

import scrapy
from bs4 import BeautifulSoup

from .decorator import start_logged
from .spider_base import SpiderBase


class _962Spider(SpiderBase):
    name = '_962'
    # 允许请求的地址, 如果请求的域名不是这个, scrapy会自动过滤掉
    allowed_domains = ['s.962.net']
    # 开始的url
    start_urls = ['http://s.962.net/sousuo/pc/?']
    # 标准URL
    base_url = "http://www.962.com/"

    def __init__(self, keyword, state_id, *args, **kwargs):
        super().__init__(keyword, state_id, *args, **kwargs)

    @start_logged
    def parse(self, response):
        params = {
            'k': self.keyword,
        }
        url = self.start_urls[0] + urlencode(params)
        yield scrapy.Request(url, callback=self.parse_document)

    def parse_document(self, response):
        # BeautifulSoup捕获数据
        content = response.body
        soup = BeautifulSoup(content, "html.parser", from_encoding='utf-8')
        # 数据清洗
        try:
            infos = soup.find(id="result").find_all("dl")
        except Exception as e:
            self.logger.critical(f"{self.__class__}查找错误。错误原因：{e}")
        else:
            for pos, info in enumerate(infos):
                # 访问info内的所有<li>标签信息爬取数据
                pos += 1
                dt = info.select(f"dl:nth-child({pos}) > dt")[0]
                dd = info.select(f"dl:nth-child({pos}) > dd")[0]
                content = dd.get_text().split("\n")
                if content is None:
                    continue

                # 生成一个数据模型
                yield self.item_opt(title=dt.a.strong.get_text(),
                                    link=dt.a["href"],
                                    content=content[5].replace(" ", "")[:-1],
                                    icon=dt.a.img["src"],
                                    source="962渠道")
