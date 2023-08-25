import os

# 请求参数清单
REQUEST_TYPE = ["GET", "PUT", "POST", "DELETE"]

# 默认的导出JSON文件格式
DEFAULT_DICT = {"URL": "", "assertion": "", "body": "", "header": "", "params": {}, "请求类型": "GET"}

# 默认导出路径
EXPORT_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "export")
if not os.path.exists(EXPORT_PATH):
    os.makedirs(EXPORT_PATH)