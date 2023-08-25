from django.urls import re_path
from inspection.consumers import LogConsumer

websocket_urlpatterns = [
    re_path(r'^log/(?P<date>.*)/(?P<source>.*)$', LogConsumer.as_asgi()),  # 登录websocket路由
    # re_path(r'^asynclog/(?P<date>.*)/(?P<source>.*)$', AsyncLogConsumer.as_asgi()) # 待实现
]
