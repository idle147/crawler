import io
import json
import logging
import os
import time

from channels.generic.websocket import (AsyncWebsocketConsumer, WebsocketConsumer)
from django.conf import settings
from inspection.models import UserModel
from inspection.views import datetime_find
from utils.thread_pool import GLOBAL_THREAD_POOL

from .config import SOURCE_CROSSWALKS

logger = logging.getLogger("Log Consumer")


class LogConsumer(WebsocketConsumer):
    """ 实时日志发送websocket """

    def connect(self):
        # 获取参数
        self.date = self.scope["url_route"]["kwargs"]["date"]
        self.source = self.scope["url_route"]["kwargs"]["source"]
        self.email = self.scope["user"].email
        # 查询文件路径
        self.job_id = self._get_info()
        log_path = os.path.join(settings.DATABASES_DIR, "crawler_logs", "piracy_crawler",
                                SOURCE_CROSSWALKS[self.source], f"{self.job_id}.log")
        self.accept()
        # 利用线程池发送
        args = [log_path]
        GLOBAL_THREAD_POOL.executor.submit(lambda p: self._send_log_info(*p), args)

    def _send_log_info(self, file_path):
        index = 0
        # 循环判断文件是否存在
        if os.path.exists(file_path) is False:
            print(f"日志文件未创建:{file_path}")
            if self.sendmsg("==== 日志文件未创建,请等待... ====") is False:
                return

        # 循环判断文件是否创建
        while True:
            time.sleep(0.5)
            if os.path.exists(file_path):
                break

        # 循环发送套接字文件信息
        with io.open(file_path, "r", encoding="utf8", errors="replace") as f:
            while True:
                if line := f.readline():
                    index = 0
                    if self.sendmsg(line) is False:
                        return
                else:
                    if index >= 50:
                        if self.sendmsg("=======断开套接字连接======") is False:
                            return
                        self.disconnect(1)
                        break
                    index += 1
                    time.sleep(0.256)

    def disconnect(self, close_code):
        # 中止执行中的Task
        print('disconnect:', self.job_id, self.channel_name)

    def sendmsg(self, message):
        msg = message.split("\n")
        try:
            self.send(text_data=json.dumps({"message": msg}))
        except Exception:
            return False
        else:
            return True

    def _get_info(self):
        user_model = UserModel.objects.get(email=self.email)
        res = datetime_find(self.date, user_model).filter(source=self.source).values("job_id")
        if len(res) == 0:
            raise ValueError("数据库查无对应的source")
        else:
            return res[0]["job_id"]


class stateConsumer(WebsocketConsumer):
    """ 更新状态"""

    def connect(self):
        # 获取参数
        self.accept()
        # 利用线程池发送
        # args = [log_path]
        # GLOBAL_THREAD_POOL.executor.submit(lambda p: self._send_log_info(*p), args)

    def disconnect(self, close_code):
        # 中止执行中的Task
        print('disconnect:', self.channel_name)

    def sendmsg(self, message):
        msg = message.split("\n")
        self.send(text_data=json.dumps({"message": msg}))


class AsyncLogConsumer(AsyncWebsocketConsumer):
    """ 异步日志发送websocket """

    async def connect(self):
        # 获取参数
        self.date = self.scope["url_route"]["kwargs"]["date"]
        self.source = self.scope["url_route"]["kwargs"]["source"]
        self.email = self.scope["user"].email
        await self.accept()

    def _get_info(self):
        user_model = UserModel.objects.get(email=self.email)
        res = datetime_find(self.date, user_model).filter(source=self.source).values("job_id")
        if len(res) == 0:
            raise ValueError("数据库查无对应的source")
        # 查询文件路径
        self.job_id = res[0]["job_id"]
        return os.path.join(settings.DATABASES_DIR, "crawler_logs", "piracy_crawler",
                            SOURCE_CROSSWALKS[self.source], f"{self.job_id}.log")

    async def disconnect(self, close_code):
        # 中止执行中的Task
        print('disconnect:', self.job_id, self.channel_name)

    async def sendmsg(self, event):
        """发送组信息

        Args:
            event (事件单元): 描述
        """
        msg = event["message"].split("\n")
        await self.send(text_data=json.dumps({"message": msg}))
