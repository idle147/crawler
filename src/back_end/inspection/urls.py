from django.urls import path

from . import views

app_name = "inspection"
urlpatterns = [
    # 当用户在浏览器中访问index/时,
    # Django将解析url,
    # 并调用执行views.py中的index视图函数。
    path('logout', views.LogOutAPIView.as_view(), name="logout"),  # 登录判断
    path('loginJudge', views.LoginStateAPIView.as_view(), name="login_judge"),  # 登录判断
    path('source', views.GetSource.as_view(), name="get_source"),  # 获取源清单
    path('start', views.StartPiracyAPIView.as_view(), name="start"),  # 启动爬虫
    path('kill', views.KillPiracyAPIView.as_view(), name="kill_piracy"),  # 结束爬虫
    path('detail', views.DetailsAPIView.as_view(), name="detail"),  # 查看详情
    path('state', views.StateAPIView.as_view(), name="state"),  # 查看状态
    path('current', views.CurrentStateAPIView.as_view(), name="state"),  # 查看某时间下的状态
    path('piracyList', views.PiracyListAPIView.as_view(), name="piracy_list"),  # 获取盗版游戏清单
    path('piracyMark', views.PiracyMarkAPIView.as_view(), name="piracy_mark"),  # 标记为盗版
    path('pieChart', views.PieChartAPIView.as_view(), name="pie_chart"),  # 获取饼图
    path('lineChart', views.LineChartAPIView.as_view(), name="line_chart"),  # 获取线图
    path('scheduled', views.ScheduledAPIView.as_view(), name="scheduled"),  # 定时计划
]
