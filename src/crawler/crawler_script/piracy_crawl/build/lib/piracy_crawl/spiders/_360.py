from urllib.parse import urlencode

import scrapy
from bs4 import BeautifulSoup

from .decorator import start_logged
from .spider_base import SpiderBase


class _360Spider(SpiderBase):
    name = '_360'
    # 允许请求的地址, 如果请求的域名不是这个, scrapy会自动过滤掉
    allowed_domains = ['zhushou.360.cn']
    # 开始的url
    start_urls = ['http://zhushou.360.cn/search/index/?']
    # 标准URL
    base_url = "http://zhushou.360.cn/"

    def __init__(self, keyword, state_id, *args, **kwargs):
        super().__init__(keyword, state_id, *args, **kwargs)

    @start_logged
    def parse(self, response):
        params = {'kw': self.keyword}
        url = self.start_urls[0] + urlencode(params)
        yield scrapy.Request(url, callback=self.parse_document)

    def parse_document(self, response):
        content = response.body
        soup = BeautifulSoup(content, "html.parser", from_encoding='utf-8')
        try:
            infos = soup.select("body > div.warp > div.main > div > ul")[0].find_all(name="li")
        except Exception:
            self.logger.critical(f"渠道[360]关键词[{self.keyword}]查找出错")
        else:
            for pos, info in enumerate(infos[:-1]):
                pos += 1
                dt = info.select(f"li:nth-child({pos}) > dl > dt")[0]
                dd = info.select(f"li:nth-child({pos}) > dl > dd")[0]
                content = dd.get_text().split("\n")
                if content is None:
                    continue
                yield self.item_opt(title=content[1],
                                    link=self.base_url + str(dt.a["href"]),
                                    content=content[3],
                                    icon=dt.a.img["_src"],
                                    source="360渠道")
