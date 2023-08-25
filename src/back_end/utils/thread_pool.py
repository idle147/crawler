

from concurrent.futures import ThreadPoolExecutor

from django.db import connections

from .singleton import SingletonType


class ThreadPool(metaclass=SingletonType):

    def __init__(self):
        # 线程池
        self.executor = ThreadPoolExecutor(20)
        # 用于存储每个项目批量任务的期程
        self.future_dict = {}

    # 检查某个项目是否有正在运行的批量任务
    def is_project_thread_running(self, project_id):
        future = self.future_dict.get(project_id, None)
        return bool(future and future.running())

    # 展示所有的异步任务
    def check_future(self):
        return {project_id: future.running() for project_id, future in self.future_dict.items()}

    def batch_thread(self):
        for conn in connections.all():
            conn.close_if_unusable_or_obsolete()

    def __del__(self):
        self.executor.shutdown()


# 主线程中的全局线程池
# global_thread_pool的生命周期是Django主线程运行的生命周期
GLOBAL_THREAD_POOL = ThreadPool()
