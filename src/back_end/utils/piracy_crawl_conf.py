

import os
import subprocess
import sys
import threading
import time

import requests
from requests.exceptions import ConnectionError
from scrapyd_api import ScrapydAPI, constants

from .singleton import SingletonType

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from web_server.settings import (CRAWLER_EGG_PATH, CRAWLER_PROJECT, LOG_DIR, SCRAPYD_PATH,
                                 SCRAPYD_URL, START_SCRAPYD)


# 爬虫服务器启动问题
class ScrapydStart():

    def __init__(self, url, auth=None):
        self.url = url
        self.auth = auth
        self.scrapyd = None
        self.current_chdir = os.getcwd()

    def _monitor_server(self):
        times = 0
        while True:
            print(f"等待启动爬虫服务器:重试次数{times}")
            if not self._judge_connect():
                times += 1
                time.sleep(3)
                continue
            else:
                # 服务器已经启动, 连接服务器
                self.scrapyd = ScrapydAPI(target=self.url, auth=self.auth)
                os.chdir(self.current_chdir)
                return self.scrapyd

    def get_scrapyd(self):
        return self.scrapyd

    def _launch(self):
        if not self._judge_connect():
            print("启动爬虫服务器")
            thread = threading.Thread(target=self._start_scrapyd)
            os.chdir(SCRAPYD_PATH)
            thread.start()
            return self._monitor_server()
        else:
            self.scrapyd = ScrapydAPI(target=self.url, auth=self.auth)
            return self.scrapyd

    def _judge_connect(self):
        try:
            requests.get(self.url)
        except ConnectionError:
            return False
        except Exception as e:
            raise IOError(f"连接爬虫服务器出现错误:{e}") from e
        else:
            return True

    def _start_scrapyd(self):
        """ 启动scrapyd """
        # 1. 线程开启进程
        print(f"线程[{threading.current_thread().getName()}]:启动scrapyd服务器")
        # 2. 创建日志文本文档
        current_time = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
        log_path = os.path.join(LOG_DIR, "scrapyd")
        if not os.path.exists(log_path):
            os.mkdir(log_path)
        stdout_ = os.path.join(log_path, f"{current_time}.txt")
        # 3. 线程监听进程是否结束
        with open(stdout_, "wb") as out:
            setting = ['DEBUG=True', 'HOST_NAME=axdda']
            subprocess.Popen("scrapyd", shell=True, stdin=sys.stdin, stdout=out, stderr=sys.stderr)


# 单例类实现一个爬虫服务器操作API
class ScrapySingleton(metaclass=SingletonType):
    FINISHED = constants.FINISHED
    RUNNING = constants.RUNNING
    PENDING = constants.PENDING

    def __init__(self):
        self.egg_path = os.path.join(CRAWLER_EGG_PATH, f'{CRAWLER_PROJECT}.egg')
        self.setup()

    def setup(self):
        scrapyd_sever = ScrapydStart(SCRAPYD_URL)
        # 主动启动服务器
        if START_SCRAPYD:
            self.scrapyd = scrapyd_sever._launch()
        else:
            self.scrapyd = scrapyd_sever._monitor_server()

        if not self.scrapyd:
            raise ValueError("获取不到爬虫服务器的信息, 请检查")
        else:
            self._project_opt()

    def get_srcapyd(self):
        return self.scrapyd

    def get_job_state(self, job_id):
        return self.scrapyd.job_status(CRAWLER_PROJECT, job_id)

    def get_list_spiders(self):
        try:
            spiders = self.scrapyd.list_spiders(CRAWLER_PROJECT)
        except Exception as e:
            if "no active project" not in str(e):
                raise ValueError(f"未知错误:{e}") from e
            self.add_egg()
            spiders = self.scrapyd.list_spiders(CRAWLER_PROJECT)
        return spiders

    def to_schedues(self, spiders, **kwargs):
        return [self.scrapyd.schedule(CRAWLER_PROJECT, spider, **kwargs) for spider in spiders]

    def to_schedue(self, spider, **kwargs):
        return self.scrapyd.schedule(CRAWLER_PROJECT, spider, **kwargs)

    def cancel_job(self, job_id):
        return self.scrapyd.cancel(CRAWLER_PROJECT, job_id)

    def _project_opt(self):
        if not self.scrapyd.list_projects():
            self.add_egg()

    def add_egg(self, egg_path=None):
        if egg_path is None:
            egg_path = self.egg_path
        with open(egg_path, "rb") as f:
            egg = f.read()
        try:
            self.scrapyd.add_version(CRAWLER_PROJECT, 1.0, egg)
        except Exception as e:
            raise SystemError(f"Scrapyd加入egg失败。原因:{e}") from e
