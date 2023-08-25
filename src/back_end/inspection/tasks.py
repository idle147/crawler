from celery import shared_task

from .views import StartPiracyAPIView


# 创建任务函数
@shared_task
def my_task():
    print('任务正在执行...')


@shared_task
def start_crawler(sources, keyword, user_id):
    # 启动爬虫
    start_piracy = StartPiracyAPIView()
    data = {"sources": sources, "keyword": keyword}
    try:
        start_piracy.start(user_id, data)
    except Exception:
        print("异步启动爬虫失败")
