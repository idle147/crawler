from urllib.parse import urlencode

import scrapy
from bs4 import BeautifulSoup

from .decorator import start_logged
from .spider_base import SpiderBase


class _5577Spider(SpiderBase):
    """ 5577爬虫很不稳定 """
    name = '_5577'
    # 允许请求的地址, 如果请求的域名不是这个, scrapy会自动过滤掉
    allowed_domains = ['s.5577.com']
    # 开始的url
    start_urls = ['http://s.5577.com/sousuo/pc/?']
    # 标准URL
    base_url = "http://www.5577.com"

    def __init__(self, keyword, state_id, *args, **kwargs):
        super().__init__(keyword, state_id, *args, **kwargs)

    @start_logged
    def parse(self, response):
        params = {
            'k': self.keyword,
        }
        url = self.start_urls[0] + urlencode(params)
        yield scrapy.Request(url, callback=self.parse_document, meta={'download_timeout': 30})

    def parse_document(self, response):
        soup = BeautifulSoup(response.body, "html.parser", from_encoding='utf-8')
        try:
            infos = soup.find(id="result").find_all("dl")
        except Exception:
            self.logger.critical(f"渠道[5577]关键词{self.keyword}查找错误。")
        else:
            if not bool(infos):
                # 没有搜索到东西
                self.logger.info(f"渠道[5577]关键词{self.keyword},查无内容")
                yield self._item_init()
            for pos, info in enumerate(infos):
                pos += 1
                dt = info.select(f"dl:nth-child({pos}) > dt")[0]
                dd = info.select(f"dl:nth-child({pos}) > dd")[0]
                content = dd.get_text().split("\n")
                if content is not None:
                    yield self._item_init(title=dt.a.strong.get_text(),
                                          link=dt.a["href"],
                                          content=content[6],
                                          icon=dd.a.img["src"])

    def _item_init(self, title="", content="", link="", icon=""):
        # 生成一个数据模型
        return self.item_opt(title=title, link=link, content=content, icon=icon, source="5577渠道")
