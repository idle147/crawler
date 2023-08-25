
from django.db import models
from django_celery_beat.models import PeriodicTask

# Create your models here.
"""
    数据表的迁移
    python manage.py makemigrations:记录对models.py的所有改动，并且将这个改动迁移到migrations这个文件下生成一个文件。
    python manage.py migrate:把这些改动作用到数据库也就是执行migrations里面新改动的迁移文件更新数据库，比如创建数据表，或者增加字段属性
"""


class UserModel(models.Model):
    """ 用户模型 """
    email = models.EmailField(verbose_name="邮箱", help_text="邮箱", unique=True, null=False)
    name = models.CharField(max_length=128, verbose_name="名字", help_text="名字", null=False)

    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name
        # 创建email索引
        indexes = [models.Index(fields=["email"])]

    def __str__(self):
        return f"{self.name}"


class StateModel(models.Model):
    """ 爬取状态清单 """

    class StateChoices(models.IntegerChoices):
        KILLED = 0
        RUNNING = 1
        FINISHED = 2

    job_id = models.CharField(max_length=32, verbose_name='job任务标识', default="")
    date = models.DateTimeField(verbose_name="创建日期")
    keyword = models.CharField(max_length=20, verbose_name='关键字')
    source = models.CharField(max_length=20, verbose_name='渠道')
    state = models.SmallIntegerField(verbose_name="状态", choices=StateChoices.choices)
    owner = models.ForeignKey(UserModel, on_delete=models.CASCADE, verbose_name="所有者")

    class Meta:
        verbose_name = "爬取状态"
        verbose_name_plural = verbose_name
        ordering = ['-date']

    def __str__(self):
        return f"{self.job_id}--{self.date}--{self.state}"


class InfoModel(models.Model):
    """ 爬虫条目 """
    title = models.CharField(max_length=128, verbose_name='标题', blank=True)
    link = models.CharField(max_length=256, verbose_name='链接', blank=True)
    content = models.CharField(max_length=256, verbose_name='描述', blank=True)
    icon = models.CharField(max_length=256, verbose_name='图标', blank=True, null=True)
    is_piracy = models.BooleanField(default=False, verbose_name='盗版标识符')
    date = models.DateTimeField(auto_now=True, verbose_name="创建日期")
    owner = models.ForeignKey(UserModel, on_delete=models.CASCADE, verbose_name="所有者")
    source_state = models.ForeignKey(StateModel, on_delete=models.CASCADE, verbose_name="爬取源")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "渠道爬取信息"
        ordering = ['source_state_id']


class ScheduledModel(models.Model):
    """ 定时计划表 """

    class StateChoices(models.IntegerChoices):
        ERROR = 0
        START = 1
        UNSTART = 2

    keyword = models.CharField(max_length=128, verbose_name='关键词', blank=True)
    sources_list = models.CharField(max_length=256, verbose_name='渠道清单',
                                    blank=True)  # 存储渠道清单, 按","分割
    schedule = models.DecimalField(max_digits=5, decimal_places=1, verbose_name="定时")
    state = models.SmallIntegerField(verbose_name="状态", choices=StateChoices.choices)
    date = models.DateTimeField(auto_now=True, verbose_name="创建日期")
    owner = models.ForeignKey(UserModel, on_delete=models.CASCADE, verbose_name="所有者")
    periodic = models.ForeignKey(PeriodicTask, on_delete=models.CASCADE, verbose_name="任务外键")
