
import os
import sys

os.chdir(os.path.dirname(__file__))

sys.path.append(os.path.join(os.path.dirname(__file__), "piracy_crawl"))
os.environ.setdefault('SCRAPY_SETTINGS_MODULE', "piracy_crawl.settings")

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


def main():
    setting = get_project_settings()
    process = CrawlerProcess(setting)
    didnt_work_spider = ['_360']

    for spider_name in process.spiders.list():
        if spider_name in didnt_work_spider:
            continue
        print(f"Running spider {spider_name}")
        process.crawl(spider_name, "1", "测试", "50")