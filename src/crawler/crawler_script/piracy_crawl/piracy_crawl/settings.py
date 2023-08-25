# Scrapy settings for piracy_crawl project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import os
import sys

import django
from django.conf import settings

# 此处借助django的model写入数据库
DJANGO_PROJECT_NAME = "back_end"
DJANGO_PROJECT_PATH = os.path.join(os.path.dirname(os.path.dirname(os.getcwd())),
                                   DJANGO_PROJECT_NAME)
sys.path.append(DJANGO_PROJECT_PATH)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "web_server.settings")
# os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

django.setup()

BOT_NAME = "piracy_crawl"

SPIDER_MODULES = ["piracy_crawl.spiders"]
NEWSPIDER_MODULE = "piracy_crawl.spiders"
"""
    日志设置, 注销掉, 因为scrapyd会帮我们生成对应的日志
"""
# now_time = time.strftime('%Y_%m_%d_%H_%M_%S', time.localtime())
LOG_LEVEL = "INFO"
# LOG_FILE = f"./scrapy_logs/scrapy_{now_time}.log"
"""
    图片抓取相关配置
"""
# 图片存储仓库
IMAGES_STORE = settings.IMAGE_ROOT
# 过期天数
IMAGES_EXPIRES = 30

# 选择自己浏览器的用户代理
USER_AGENT = (
    r"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
)
USER_AGENT_LIST = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
]

# 是否运行机器人规则(君子协议)
ROBOTSTXT_OBEY = False

# 配置Scrapy执行的最大并发请求数(默认:16)
CONCURRENT_REQUESTS = 16

# 配置线程池
REACTOR_THREADPOOL_MAXSIZE = 10

# 配置同一个网站的请求延迟 (默认: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
DOWNLOAD_DELAY = 3

# 域级别的最大并发请求数(默认: 8)
CONCURRENT_REQUESTS_PER_DOMAIN = 8

# IP级别的最大并发请求数(默认: 0)(与域级别互斥)
# CONCURRENT_REQUESTS_PER_IP = 5

# 启动cookies (默认:True)
# 由于不需要登录就能搜索信息,所以禁用cookie
COOKIES_ENABLED = False

# 启动控制台 (默认: True)
TELNETCONSOLE_ENABLED = False

# 覆盖默认的请求头:
# DEFAULT_REQUEST_HEADERS = {
#     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
#     'Accept-Language': 'zh-CN,zh;q=0.9',
#     'Connection': 'keep-alive'
# }
"""
    中间键与扩展启动部分
    See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
    See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
    See https://docs.scrapy.org/en/latest/topics/extensions.html
    See https://docs.scrapy.org/en/latest/topics/item-pipeline.html   
"""
# spider中间键的启动
# SPIDER_MIDDLEWARES = {
#    'piracy_crawl.middlewares.inspectionSpiderMiddleware': 543,
# }

# spider下载中间键的启动
DOWNLOADER_MIDDLEWARES = {
    'piracy_crawl.middlewares.PiracyCrawlDownloaderMiddleware': 543,
}

# 扩展的启用
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# 配置pipelines的启动
ITEM_PIPELINES = {
    "piracy_crawl.pipelines.CoverPipeline": 1,
    "piracy_crawl.pipelines.PiracyCrawlPipeline": 300,
}
"""
    节流处理部分
    See https://docs.scrapy.org/en/latest/topics/autothrottle.html
"""
# 自动节流爬取速度扩展 (disabled by default)
# AUTOTHROTTLE_ENABLED = True

# 初始下载延迟
# AUTOTHROTTLE_START_DELAY = 5

# 在高延迟情况下设置的最大下载延迟
# AUTOTHROTTLE_MAX_DELAY = 60

# 向每个远程服务器并行发送的平均请求数
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0

# 显示每一个收到的响应的节流统计信息
# AUTOTHROTTLE_DEBUG = False
"""
    HTTP缓存配置功能
    See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
"""
# HTTP的缓存配置 (disabled by default)
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
