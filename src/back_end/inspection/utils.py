import logging

from rest_framework.exceptions import NotAuthenticated
from rest_framework.request import Request

from .models import UserModel

logger = logging.getLogger("log")


def login_judge(func):

    def wrapper(*args, **kwargs):
        user_info = args[1].user
        if user_info.is_anonymous:
            raise NotAuthenticated("未登录")
        if isinstance(args[1], Request):
            user_judge(args[1])
        else:
            raise ValueError("登录判断参数错误")
        return func(*args, **kwargs)

    return wrapper


def get_ip_add(request):
    return request.META.get('HTTP_X_FORWARDED_FOR') or request.META.get('REMOTE_ADDR')


def user_judge(request):
    user = request.user
    email_address = getattr(user, user.get_email_field_name())
    id_address = get_ip_add(request)

    try:
        user_object = UserModel.objects.get(email=email_address)
    except UserModel.DoesNotExist:
        user_object = UserModel(email=email_address, name=user.get_username())
        user_object.save()
        logger.info(
            f"IP地址[{id_address}]注册新用户。ID:{user.id}, 用户名:{user.get_username()}, 邮箱地址:{email_address}"
        )
    return user_object


def sources_list_clean(sources_list):
    new_sources_list = []
    for source in sources_list:
        if source.startswith("_"):
            new_sources_list.append(source[1:])
        else:
            new_sources_list.append(source)
    return new_sources_list
