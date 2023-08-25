import json

import pytz
from django_celery_beat.models import (CrontabSchedule, IntervalSchedule, PeriodicTask)


class ScheduleOpt:

    def __init__(self) -> None:
        pass

    # 创建间隔性任务
    def create_interval_minutes(self, interval, *args, **kwargs):
        """ 间隔性任务

        Args:
            interval: 间隔时间
        """
        # # 周期性任务可选参数
        # IntervalSchedule.DAYS #固定间隔天数
        # IntervalSchedule.HOURS #固定间隔小时数
        # IntervalSchedule.MINUTES #固定间隔分钟数
        # IntervalSchedule.SECONDS #固定间隔秒数
        # IntervalSchedule.MICROSECONDS #固定间隔微秒
        schedule, created = IntervalSchedule.objects.get_or_create(every=interval,
                                                                   period=IntervalSchedule.MINUTES)
        # 提供参数
        return PeriodicTask.objects.create(interval=schedule,
                                           task='inspection.tasks.start_crawler',
                                           args=json.dumps(args),
                                           kwargs=json.dumps(kwargs),
                                           description=f"每{interval}分钟定时启动爬虫")

    # 创建周期任务
    def create_crontab_hours(self, interval, **kwargs):
        """ 周期性任务

        Args:
            interval: 周期时间
        """
        crontab, _ = CrontabSchedule.objects.update_or_create(
            minute="*",
            hour=f"{interval}",
            day_of_week="*",
            day_of_month='*',
            month_of_year='*',
            timezone=pytz.timezone("Asia/Shanghai"),
        )

        # 如果任务存在就更新，不存在则创建
        PeriodicTask.objects.update_or_create(
            defaults={
                "interval": crontab,
                "task": "inspection.tasks.start_crawler",  # 指定需要周期性执行的任务
                "kwargs": json.dumps(kwargs, ensure_ascii=False)  # 传入的参数
            })

    # 删除任务
    def delete_task(self, id):
        if task := PeriodicTask.objects.filter(id=id):
            task.update(enabled=False)
            task.delete()

    # 暂停任务
    def pause_task(self, sub_id, status):
        if tasks := PeriodicTask.objects.filter(name__startswith=sub_id):
            tasks.update(enabled=bool(status))
