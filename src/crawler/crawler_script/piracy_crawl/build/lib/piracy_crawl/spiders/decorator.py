from functools import wraps


def start_logged(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        func_self = args[0]
        func_self.logger.info(f"==== 开始爬取{func_self.name}游戏信息 ====")
        return func(*args, **kwargs)

    return wrapper