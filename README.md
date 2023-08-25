# 环境说明

1. 后端：python3.9 + django4.0.7 + channels + celery + django-celery + celery-results + sqlite3
2. 爬虫：Scrapy2.6.2  + scrapyd1.3.0
3. 前端：vue3+ts
4. 客户端：pyqt
5. 操作系统：win10



# 快速部署说明

1. 安装后端依赖
2. 进入后端文件夹：输入下述指令（定时任务请启动redis服务）

```
python manage.py runserver
Celery -A web_server worker -l info -P eventlet
celery -A web_server beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
```

3. 安装前端依赖
4. 进入前端文件夹: 输入下述指令

```
npm run serve
```

5. 浏览器输入：localhost:8080



# 详细部署说明

## 爬虫（可选）

**注意：爬虫已经接入了后端，配合后端一键启动。该部分可以略过**

### 爬虫服务器(可选)

#### 启动

1. 关于爬虫服务器已经整合进后端里, **往往不需要单独启动**。【当然你想我也不阻止:)】
2. 修改后端django的设置文件，见下面**后端启动说明**
3. 进入爬虫文件夹：crawler/crawler_server
4. 输入指令：scrapyd &

#### 配置参数说明

配置参数位置: crawler/crawler_server/scrapyd.conf

```
[scrapyd]
# 网页和Json服务监听的IP地址，默认为127.0.0.1
bind_address = 127.0.0.1

# 监听的端口，默认为6800
http_port = 6800

# 是否打开debug模式，默认为off
debug = off

# 每个CPU可启用的Scrapy 进程数，默认为4
max_proc_per_cpu = 4

# 可启用的最多进程数，默认为0.如果未设置或者设为0，则使用的最多进程数=CPU数量*max_proc_per_cpu
max_proc = 0

# 项目eggs生成目录，默认为项目目录下eggs
eggs_dir = eggs

# 项目日志生成目录，默认为项目目录下logs，如果不想要生成日志，可以直接设置成空
logs_dir = ../../database/crawler_logs

# 项目dbs生成目录，默认为项目目录下dbs
dbs_dir = dbs

# 爬取的items存储的文件夹（版本0.15.以上），默认为空，不存储。
items_dir =

# 每个爬虫保持的完成任务数，默认为5.（版本0.15.以上，以前版本中为logs_to_keep）
jobs_to_keep = 5

# 保持的完成任务进程数。默认为100.（版本0.14.以上）
finished_to_keep = 100

# 轮训请求队列的时间间隔。默认为5s，可以为浮点数
poll_interval = 5.0

# 启动子进程的模块。可以使用自定义
runner = scrapyd.runner

# 返回可用于twisted的application，可继承于Scrapyd添加和移除自己的组件和服务。 https://twistedmatrix.com/documents/current/core/howto/application.html查看更多
application = scrapyd.app.application
launcher = scrapyd.launcher.Launcher

# twisted的web资源，表示到scrapyd的接口。Scrapyd包含一个带有网站的界面，可以提供对应用程序的web资源的简单监视和访问。此设置必须提供twisted web资源的根类。
webroot = scrapyd.website.Root

[services]
schedule.json = scrapyd.webservice.Schedule
cancel.json = scrapyd.webservice.Cancel
addversion.json = scrapyd.webservice.AddVersion
listprojects.json = scrapyd.webservice.ListProjects
listversions.json = scrapyd.webservice.ListVersions
listspiders.json = scrapyd.webservice.ListSpiders
delproject.json = scrapyd.webservice.DeleteProject
delversion.json = scrapyd.webservice.DeleteVersion
listjobs.json = scrapyd.webservice.ListJobs
daemonstatus.json = scrapyd.webservice.DaemonStatus
```

#### POST格式

```python
import requests
 
adder='http://127.0.0.1:6800'
data = {
        'project':'piracy_crawl',
        'spider':["_360","_4399"],
        'setting':['DOWNLOAD_DELAY=3','CONCURRENT_REQUESTS=32'],
        'arg1':1,
        'arg2':"阴阳师"
}
resp = requests.post(adder,data=data)
```

#### CURL格式

```
# 启动
curl http://127.0.0.1:6800/schedule.json -d project=default -d spider=<爬虫的名字> -d setting=DOWNLOAD_DELAY=<爬虫时间延迟> -d arg1=<参数>

curl http://127.0.0.1:6800/schedule.json -d project=piracy_crawl -d spider="_360" -d setting=DOWNLOAD_DELAY=2 -d param=user_id=1,keyword=阴阳师

# 取消
curl http://localhost:6800/cancel.json -d project=project -d job=<job_id>

# 列出项目jobs
curl http://localhost:6800/listjobs.json?project=piracy_crawl | python -m json.tool
```

### 爬虫脚本(可选)

**项目已经打包好了**，见：/crawler/crawler_script/egg

重新打包需要将egg部署到爬虫服务器上，否则会出现谜之错误

#### 流程

2. 进入爬虫路径: ./crawler/crawler_script/piracy_crawl
3. 输入指令启动爬虫客户机: scrapyd-deploy --build-egg="../egg/piracy_crawler.egg"
4. 操作爬虫

#### 命令解释

Scrapyd-deploy <target> -p <project> --version <version> --build-egg <egg_path>

* target：deploy后面的名称。
* project：自行定义名称，跟爬虫的工程名字无关。
* version：自行定义版本号，不写的话默认为当前时间戳
* egg_path: 打包的egg的地址:[--build-egg="../egg/piracy_crawler.egg"]

[官方文档](https://scrapyd.readthedocs.io/en/stable/api.html)

## 后端

### 启动说明

1. 进入虚拟环境（依赖见 src/back_end/requirements.txt）
2. 进入back_end文件夹
3. **顺序启动相应组件: redis --> django --> celery --> celery_beat**

注: 启动django会顺带启动爬虫服务器, 请保证文件结构的一致性。若想独立部署爬虫服务器，请更改django的setting文件

URL： back_end/web_server/setting.py

```python
# scrapyd相关配置
START_SCRAPYD = True  # 是否交由django启动scrapyd
SCRAPYD_URL = "http://127.0.0.1:6800"
SCRAPYD_PATH = os.path.join(os.path.dirname(BASE_DIR), "crawler", "crawler_server")

# 向scrapyd提交的EGG路径
CRAWLER_EGG_PATH = os.path.join(os.path.dirname(BASE_DIR), "crawler", "crawler_script", "egg")
CRAWLER_PROJECT = "piracy_crawler"
```

### Redis启动

1. 进入redis安装目录 cd redis
2. 输入 redis-server.exe redis.windows.conf 启动redis命令，看是否成功
3. 可能会启动失败，报错:**28 Nov 09:30:50.919 # Creating Server TCP listening socket 127.0.0.1:6379: bind: No error**
4. 报错后，输入redis-cli.exe
6. 输入shutdown 结束
7. 输入 exit 退出
8. 继续输入 redis-server.exe redis.windows.conf 启动redis命令，启动成功。

### Django启动指令

1. 进入虚拟环境
2. 进入back_end文件夹
3. 输入指令

```
python manage.py runserver
```

### Celery启动指令

1. 进入虚拟环境
2. 进入back_end文件夹
3. 输入指令

```
Linux下测试，启动Celery
Celery -A web_server worker -l info
​
Windows下测试，启动Celery [异步任务和计划任务]
Celery -A web_server worker -l info -P eventlet
​
如果Windows下Celery不工作，输入如下命令
Celery -A web_server worker -l info --pool=solo
```

### Celery_Beat启动指令

1. 进入虚拟环境
2. 进入back_end文件夹
3. 输入指令

```
celery -A web_server beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
```



## 前端

### 启动说明

1. 进入front_end文件夹
3. 安装依赖
4. 输入指令: npm run serve
5. 网站地址： http://localhost:8080/

# 客户端使用说明

### 启动说明

1. 双击src/client/bin/接口测试工具.exe
2. 右键左侧的接口分组管理页面【空白区域】可实现 **创建任务组** 功能
3. 在 **创建任务组** 条目上右键 选择【创建接口】
4. 点击【完成】保存
5. 点击【执行测试】通过下拉框【选择任务组】进行接口测试

### 导入模板

1. 导入模板文件位于: src/client/bin/export
2. 请保证cookie存放于Header位置（为了配合接口测试，后端设置了一个永不过期的cookie）
3. 请确保Header、params、body内容符合Json语法
4. 请确保Assertion为python的list数据结构，所有的断言请保证结果为True
5. 基于POST、PUT、DELETE请求，请确保获取XCSRF_token，详见接口文档



