# gunicorn_config.py
import logging
import logging.handlers
import multiprocessing
import os
from logging.handlers import WatchedFileHandler

bind = '0.0.0.0:8000'  # 绑定ip和端口号
# chdir = '/opt/workspace/bookstore'  # 目录切换
# backlog = 500              # 监听队列
timeout = 60  # 超时
worker_class = 'gevent'  # 使用gevent模式，还可以使用sync 模式，默认的是sync模式
workers = multiprocessing.cpu_count() * 2 + 1  # 进程数
threads = 5  # 指定每个进程开启的线程数
loglevel = 'info'  # 日志级别，这个日志级别指的是错误日志的级别，而访问日志的级别无法设置
access_log_format = '%(t)s %(p)s %(h)s "%(r)s" %(s)s %(L)s %(b)s %(f)s" "%(a)s"'
accesslog = "./log/gunicorn_access.log"  # 访问日志文件
errorlog = "./log/gunicorn_error.log"  # 错误日志文件
proc_name = 'gunicorn_project'  #进程名
