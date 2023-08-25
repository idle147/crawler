
import os

from celery import Celery, platforms

# 设置环境变量
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web_server.settings')

# 实例化

app = Celery('web_server', backend='redis', broker='redis://localhost')  # redis做MQ配置

# namespace='CELERY'作用是允许你在Django配置文件中对Celery进行配置
# 但所有Celery配置项必须以CELERY开头，防止冲突
app.config_from_object('django.conf:settings', namespace='CELERY')

# 自动从Django已注册app的app中,发现task.py
app.autodiscover_tasks()

platforms.C_FORCE_ROOT = True  #root用户启动需要加上这一行
