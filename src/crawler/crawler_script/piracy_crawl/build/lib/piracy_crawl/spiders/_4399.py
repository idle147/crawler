from urllib.parse import urlencode

import scrapy
from bs4 import BeautifulSoup

from .decorator import start_logged
from .spider_base import SpiderBase


class _4399Spider(SpiderBase):
    name = '_4399'
    # 允许请求的地址, 如果请求的域名不是这个, scrapy会自动过滤掉
    allowed_domains = ['www.4399.cn']
    # 开始的url
    start_urls = ['http://www.4399.cn/search.html?']
    # 标准URL
    base_url = "http://zhushou.4399.cn/"

    def __init__(self, keyword, state_id, *args, **kwargs):
        super().__init__(keyword, state_id, *args, **kwargs)

    @start_logged
    def parse(self, response):
        params = {
            'type': 'game',
            'w': self.keyword,
        }
        url = self.start_urls[0] + urlencode(params)
        yield scrapy.Request(url, callback=self.parse_document)

    def parse_document(self, response):
        # BeautifulSoup捕获数据
        content = response.body
        soup = BeautifulSoup(content, "html.parser", from_encoding='utf-8')
        # 数据清洗
        try:
            infos = soup.select("body > div.f-conwrap.f-tab > div.f-tabcon > ul")[0].find_all(
                name="li")
        except Exception:
            self.logger.critical(f"渠道[4399]关键词{self.keyword}查找错误。")
        else:
            for pos, info in enumerate(infos):
                # 访问info内的所有<li>标签信息爬取数据
                pos += 1
                m_name = info.select(f"li:nth-child({pos}) > h4 > a")[0]
                m_icon = info.select(f"li:nth-child({pos}) > a > img")[0]
                m_info = info.select(f"li:nth-child({pos}) > div.m-info")[0]

                # 生成一个数据模型
                yield self.item_opt(title=m_name["title"],
                                    link=self.base_url + m_name["href"],
                                    content=m_info.get_text().split(" ")[2],
                                    icon=m_icon["data-src"],
                                    source="4399渠道")
