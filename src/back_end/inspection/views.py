import os
import sys
import time
from sqlite3 import OperationalError

from django.conf import settings
from django.contrib.auth import logout
from django.db.models import Count
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone
from django.middleware.csrf import get_token

from rest_framework import exceptions, status
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from .config import SCHEDULE_STATE, SOURCE_CROSSWALKS, STATE
from .models import InfoModel, ScheduledModel, StateModel, UserModel
from .schedule import ScheduleOpt
from .serializers import InfoSerializer, PiracySerializer, ScheduledSerializer, StateSerializer
from .utils import logger, login_judge, user_judge

# 引用上级目录的文件
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.piracy_crawl_conf import ScrapySingleton
from utils.thread_pool import GLOBAL_THREAD_POOL


def datetime_find(date, owner):
    """根据日期查找数据库

    Args:
        date (string): 日期
        owner (UserModel.id): 用户模型

    Raises:
        exceptions.ParseError: 日期不符合setting内设置的格式
        exceptions.ParseError: 数据库查无错误
        exceptions.ParseError: 兜底异常
    """
    # 3. 查找数据库
    try:
        start_time = timezone.datetime.strptime(date, settings.DATETIME_FORMAT)
        start_time.astimezone(timezone.utc)
    except Exception as e:
        raise exceptions.ParseError(f"date格式错误,参考格式:{settings.DATETIME_FORMAT}") from e
    try:
        end_time = start_time + timezone.timedelta(seconds=1)
        state_models = StateModel.objects.filter(date__range=(start_time, end_time), owner=owner)
    except StateModel.DoesNotExist as e:
        raise exceptions.ParseError("数据库查无数据") from e
    except Exception as e:
        logger.info(f"杀死爬虫出现未知错误:{e}")
        raise exceptions.ParseError("未知错误") from e
    else:
        return state_models


class JSONResponse(HttpResponse):
    """
    将内容渲染为JSON的HttpResponse对象。
    """

    def __init__(self, data=None, msg="", state_num=status.HTTP_200_OK, **kwargs):
        if data is None:
            data = {}
        json_info = {"message": msg, "content": data}
        content = JSONRenderer().render(json_info)
        kwargs['content_type'] = 'application/json'
        kwargs['charset'] = 'utf-8'
        kwargs['status'] = state_num
        super().__init__(content, **kwargs)


class LogOutAPIView(APIView):
    """ 登出判断 """

    def get(self, request):
        logout(request)
        return HttpResponseRedirect(redirect_to='/')


class LoginStateAPIView(APIView):
    """ 判断是否登录, 返回用户名 """

    def get(self, request):
        if not request.user.is_authenticated:
            raise exceptions.AuthenticationFailed("未登录")
        user_model = user_judge(request)
        ret = {"message": "已登录", "username": user_model.name}
        if str(request.user) == "XXX":
            ret["token"] = get_token(request)
        return Response(ret, status=status.HTTP_200_OK)


class GetSource(APIView):
    pyd_singleton = ScrapySingleton()
    source_table = SOURCE_CROSSWALKS.inverse

    @login_judge
    def get(self, request):
        """ 获取源清单 """
        try:
            source_list = self.pyd_singleton.get_list_spiders()
        except Exception:
            self.pyd_singleton.add_egg()
            try:
                source_list = self.pyd_singleton.get_list_spiders()
            except Exception:
                return exceptions.APIException("爬虫服务器启动异常")
        else:
            data = [self.source_table[source] for source in source_list]
            return Response({"message": "success", "source": data}, status=status.HTTP_200_OK)


class DetailsAPIView(APIView):
    """ 获取当前用户所选爬虫的详细信息
    {
        "data": "2022-08-19 21:00:21"
    }
    """

    @login_judge
    def get(self, request):
        param = request.query_params
        if "date" not in param:
            raise exceptions.ParseError("参数错误")
        msg = "success"
        data = None
        if user_object := user_judge(request):
            # 查询time所对应的id
            state_models = datetime_find(param["date"], user_object)
            id_list = [state_model.id for state_model in state_models]
            if not id_list:
                raise exceptions.NotFound("查无结果")
            try:
                info = InfoModel.objects.filter(source_state_id__in=id_list, owner=user_object)
                serializer = InfoSerializer(info, many=True)
            except InfoModel.DoesNotExist as e:
                raise exceptions.NotFound("查无结果") from e
            except Exception:
                msg = "error"
            else:
                data = serializer.data
            return JSONResponse(data, msg=msg, state_num=status.HTTP_200_OK)


class StateAPIView(APIView):
    """ 获取当前用户所有的状态信息 """

    def _get_source_state(self, obj):
        source = []
        state = []
        for level in obj:
            # 状态判断
            source.append(level.source)
            state.append(level.state)

        # 状态校验
        if 0 in state:
            return source, STATE[0]
        elif 1 in state:
            return source, STATE[1]
        else:
            return source, STATE[2]

    @login_judge
    def get(self, request):
        data = []
        msg = "success"
        if user_object := user_judge(request):
            try:
                infos = StateModel.objects.filter(owner=user_object).values(
                    "date", "owner_id", "keyword").distinct()

                for info in infos:
                    second_level = StateModel.objects.filter(owner_id=info["owner_id"],
                                                             date=info["date"])
                    res = self._get_source_state(second_level)
                    local_time = timezone.localtime(info["date"])
                    data.append({
                        "date": local_time.strftime(settings.DATETIME_FORMAT),
                        "keyword": info["keyword"],
                        "source": res[0],
                        "state": res[1]
                    })
            except StateModel.DoesNotExist as e:
                raise exceptions.NotFound("查无结果") from e
            except Exception:
                msg = "error"
        return Response({"message": msg, "content": data}, status=status.HTTP_200_OK)


class StartPiracyAPIView(APIView):
    """ 启动爬虫
    {
        "sources":["360渠道", "4399渠道"],
        "keyword": "XXXX"
    }
    """
    # 实例化一个爬虫服务器API接口
    pyd_singleton = ScrapySingleton()

    @login_judge
    def post(self, request):
        # 1.接收参数
        dict_info = request.data
        # 2. 参数检查
        if "sources" not in dict_info:
            raise exceptions.ParseError("渠道选择参数错误")
        for source in dict_info["sources"]:
            if source not in SOURCE_CROSSWALKS:
                raise exceptions.ParseError(f"所选的渠道{source}错误, 尚无该渠道的爬虫")
        if "keyword" not in dict_info:
            raise exceptions.ParseError("没有选择搜索关键词")

        # 3. 告知爬虫, 写入数据库
        return self.start(request.user.id, dict_info)

    def start(self, user_id, dict_info):
        current_time = timezone.now()
        logger.info(f"用户ID[{user_id}]启动爬虫, 关键词[{dict_info['keyword']}], 渠道{dict_info['sources']}")

        # 获取用户模型
        try:
            owner = UserModel.objects.get(id=user_id)
        except UserModel.DoesNotExist as e:
            logger.error(f"创建爬虫方案时查无用户id[{user_id}], 错误原因: {e}")
            raise exceptions.APIException(f"创建爬虫方案时查无用户id[{user_id}]") from e

        try:
            args = [current_time, dict_info["sources"], owner, dict_info["keyword"]]
            GLOBAL_THREAD_POOL.executor.submit(lambda p: self._start_schedule(*p), args)
        except Exception as e:
            logger.error(f"用户ID[{user_id}]爬虫启动失败, 错误原因: {e}")
            raise exceptions.APIException("爬虫启动失败") from e
        else:
            # 交由前端轮询数据库
            return Response(
                {
                    "message": "爬虫创建成功",
                    "date": f"{current_time.strftime(settings.DATETIME_FORMAT)}"
                },
                status=status.HTTP_201_CREATED)

    def _start_schedule(self, added_date, sources, owner, point_word):
        """ 线程函数, 启动爬虫 """
        # 1. 创建爬虫实例
        jobs = []
        for source in sources:
            job_model = StateModel(date=added_date,
                                   keyword=point_word,
                                   source=source,
                                   state=StateModel.StateChoices.RUNNING,
                                   owner=owner)
            job_model.save()
            # 创建爬虫实例
            job_id = self.pyd_singleton.to_schedue(
                SOURCE_CROSSWALKS[source],  # 传递的是爬虫的名字, 没有加"渠道"二字
                keyword=point_word,
                state_id=job_model.id)
            job_model.job_id = job_id
            job_model.save()
            jobs.append(job_id)

        # 3. 循环验证是否爬取完毕
        while True:
            running_jobs = []
            # 循环遍历模型是否完成
            for job in jobs:
                state = self.pyd_singleton.get_job_state(job)
                if state in [self.pyd_singleton.RUNNING, self.pyd_singleton.PENDING]:
                    running_jobs.append(job)
                else:
                    state_model = StateModel.objects.get(job_id=job)
                    # 此处判断以规避中止状态
                    if state_model.state == StateModel.StateChoices.RUNNING:
                        state_model.state = StateModel.StateChoices.FINISHED
                        state_model.save()

            # 只对运行的模型进行处理
            jobs = running_jobs

            # 全部执行完毕, 结束循环
            if not running_jobs:
                return

            time.sleep(0.5)


class CurrentStateAPIView(APIView):
    """获取当前时间点下的状态信息
    {
        "data": "2022-08-19 21:00:21"
    }
    """

    @login_judge
    def get(self, request):
        # 1. 接收参数
        dict_info = request.query_params
        # 2. 参数校验
        if "date" not in dict_info:
            raise exceptions.ParseError("缺少date参数")
        user_object = user_judge(request)
        info = datetime_find(dict_info["date"], user_object)
        serializer = StateSerializer(info, many=True)
        return JSONResponse(serializer.data, msg="success", state_num=status.HTTP_200_OK)


class KillPiracyAPIView(APIView):
    """ 中止爬虫
    {"date": "2022-09-02 12:12:12"}
    """

    # 实例化一个爬虫服务器API接口
    pyd_singleton = ScrapySingleton()

    @login_judge
    def put(self, request):
        # 1.接收参数
        dict_info = request.data

        # 2.参数校验
        if "date" not in dict_info:
            raise exceptions.ParseError("没有date参数")

        # 3. 查找数据库
        user_object = user_judge(request)
        state_models = datetime_find(dict_info["date"], user_object)

        # 4. 中止爬虫
        for state_model in state_models:
            state = self.pyd_singleton.cancel_job(state_model.job_id)
            if state is None or state != "running":
                current_state = StateModel.objects.get(id=state_model.id, owner=request.user.id)
                if current_state.state == StateModel.StateChoices.KILLED:
                    state_model.state = StateModel.StateChoices.KILLED
                    state_model.save()
                    return Response({"message": "爬虫已被终止"}, status=status.HTTP_200_OK)
                elif current_state.state == StateModel.StateChoices.FINISHED:
                    continue
            # 5. 写入数据库
            state_model.state = StateModel.StateChoices.KILLED
            state_model.save()

        return Response({"message": "爬虫终止成功"}, status=status.HTTP_200_OK)


class PiracyListAPIView(APIView):
    """ 查看盗版详情接口 """

    @login_judge
    def get(self, request):
        # 查找数据库
        info = InfoModel.objects.filter(owner=request.user.id, is_piracy=True)
        serializer = PiracySerializer(info, many=True)
        return JSONResponse(serializer.data, msg="success", state_num=status.HTTP_200_OK)


class PiracyMarkAPIView(APIView):
    """ 标记盗版
    { "id": num }
    """

    @login_judge
    def put(self, request):
        # 1.接收参数
        dict_info = request.data

        # 2.参数校验
        if "id" not in dict_info:
            raise exceptions.ParseError("id参数缺失")
        try:
            id_info = int(dict_info["id"])
        except Exception as e:
            raise exceptions.ParseError("id参数错误") from e

        # 3. 查找数据库
        try:
            info = InfoModel.objects.get(id=id_info, owner=request.user.id)
        except StateModel.DoesNotExist as e:
            raise exceptions.MethodNotAllowed("数据库查无信息") from e
        else:
            if info.is_piracy:
                return Response({"message": "success", "id": id_info}, status=status.HTTP_200_OK)
            info.is_piracy = True
            info.save()
            return Response({"message": "success", "id": id_info}, status=status.HTTP_200_OK)


class PieChartAPIView(APIView):

    @login_judge
    def get(self, request):
        # 查找数据库
        count_set = InfoModel.objects.filter(
            owner=request.user.id,
            is_piracy=True).values("source_state_id").annotate(count=Count("source_state_id"))

        res = []
        for item in count_set:
            state_model = StateModel.objects.get(id=item["source_state_id"])
            res.append({"name": state_model.source, "value": item["count"]})
        return Response({"message": "success", "content": res}, status=status.HTTP_200_OK)


class LineChartAPIView(APIView):
    """ 获取线图数据 """

    @login_judge
    def get(self, request):
        # 查找数据库
        ret = []

        query_res = InfoModel.objects.filter(owner=request.user.id, is_piracy=True).values(
            "source_state_id", "date__date").annotate(nums=Count("date__date"))

        # 求取时间集合
        time_set = list(set(query_res.values_list("date__date")))
        source_set = list(set(query_res.values_list("source_state_id")))

        # 拆分写入
        for source_id in source_set:
            state_model = StateModel.objects.get(id=source_id[0])
            for time_info in time_set:
                try:
                    info = query_res.get(source_state_id=source_id, date__date=time_info[0])
                except InfoModel.DoesNotExist:
                    ret.append({
                        "source": state_model.source,
                        "date": str(time_info[0]),
                        "count": 0
                    })
                else:
                    ret.append({
                        "source": state_model.source,
                        "date": str(time_info[0]),
                        "count": info["nums"]
                    })
        x_axis = [str(time[0]) for time in time_set]
        return Response({
            "message": "success",
            "x_axis": x_axis,
            "content": ret
        },
                        status=status.HTTP_200_OK)


class ScheduledAPIView(APIView):
    """ 定时任务接口 """
    SCHEDULE = ScheduleOpt()

    @login_judge
    def get(self, request):
        """ 获取定时计划清单 """
        try:
            infos = ScheduledModel.objects.filter(owner_id=request.user.id)
            serializer = ScheduledSerializer(infos, many=True)
        except ScheduledModel.DoesNotExist as e:
            raise exceptions.NotFound("查无结果") from e
        except Exception as e:
            raise exceptions.APIException("未知错误") from e
        else:
            data = serializer.data
            return JSONResponse(data, msg="success", state_num=status.HTTP_200_OK)

    @login_judge
    def post(self, request):
        """ 加入定时任务
        {
            "keyword": "荒野行动",
            "source": ["360渠道", "4399渠道"],
            "time": 1.0,
        }
        """
        # 1.接收参数
        dict_info = request.data

        # 2.参数校验
        if "keyword" not in dict_info:
            raise exceptions.ParseError("keyword参数缺失")

        if "sources" not in dict_info:
            raise exceptions.ParseError("sources参数缺失")

        for source in dict_info["sources"]:
            if source not in SOURCE_CROSSWALKS:
                raise exceptions.ParseError(f"所选的渠道{source}错误, 尚无该渠道的爬虫")
        sources_str = ",".join(dict_info["sources"])

        if "time" not in dict_info:
            raise exceptions.ParseError("time参数缺失")
        try:
            time_info = round(float(dict_info["time"]), 1)
        except Exception as e:
            raise exceptions.ParseError("time参数错误") from e

        # 3. 查找数据库
        if user_object := user_judge(request):
            try:
                param = {
                    "keyword": dict_info["keyword"],
                    "sources": dict_info["sources"],
                    "user_id": user_object.id
                }
                schedule_model = self.SCHEDULE.create_interval_minutes(interval=time_info * 60,
                                                                       **param)
                info = ScheduledModel(keyword=dict_info["keyword"],
                                      sources_list=sources_str,
                                      schedule=time_info,
                                      state=ScheduledModel.StateChoices.START,
                                      owner=user_object,
                                      periodic=schedule_model)
                info.save()
            except Exception as e:
                raise exceptions.APIException(f"未知错误{e}") from e
            else:

                return Response(
                    {
                        "message": "success",
                        "id": info.id,
                        "state": SCHEDULE_STATE[info.state]
                    },
                    status=status.HTTP_200_OK)
        return exceptions.APIException("查无用户列表, 请检查服务器")

    @login_judge
    def delete(self, request):
        # 定义默认参数
        times = 5
        # 1.接收参数
        dict_info = request.data
        # 2. 参数校验
        if "id" not in dict_info:
            raise exceptions.ParseError("缺少id参数")
        try:
            schedule_id = int(dict_info["id"])
        except Exception as e:
            raise exceptions.ParseError("id参数错误") from e
        else:
            while times >= 0:
                try:
                    info = ScheduledModel.objects.get(id=schedule_id)
                    info.periodic.delete()
                except ScheduledModel.DoesNotExist as exc:
                    raise exceptions.ParseError(f"id[{schedule_id}]查无数据") from exc
                except OperationalError:
                    time.sleep(0.5)
                    times -= 1
                    continue
                except Exception as exc:
                    raise exceptions.APIException(f"{schedule_id}删除失败") from exc
                else:
                    return Response({"message": "success"}, status=status.HTTP_200_OK)