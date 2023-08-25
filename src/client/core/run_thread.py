import time

import requests
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QMessageBox
from collections.abc import Iterable

from .config import REQUEST_TYPE


class SubThread(QThread):
    # 自定义信号
    SIGNAL_DONE = pyqtSignal(str, dict)

    def __init__(self, interface_dict, parent):
        super(SubThread, self).__init__(parent)
        self.interface_dict = interface_dict
        self.stop_flag = False
        self.parent = parent
        parent.STOP_THREAD.connect(self.stop_test)

    def set_identity(self, text):
        # 设置多线程名称
        self.identity = text

    def run(self):
        self.start_test()

    def stop_test(self):
        self.stop_flag = True

    def start_test(self):
        """ 启动测试 """
        res_detail = {}
        for key in self.interface_dict:
            time_start = time.time()

            # URL参数校验
            try:
                url = self.interface_dict[key]["URL"]
            except Exception:
                QMessageBox.critical(self.parent, "接口测试", f"[{key}]缺少[URL]", QMessageBox.Yes,
                                     QMessageBox.Yes)
                continue

            # 请求类型参数校验
            try:
                request_type = self.interface_dict[key]["请求类型"]
            except Exception:
                QMessageBox.critical(self.parent, "接口测试", f"[{key}]缺少[请求类型]", QMessageBox.Yes,
                                     QMessageBox.Yes)
                continue
            else:
                if request_type not in REQUEST_TYPE:
                    QMessageBox.critical(self.parent, "接口测试", f"[{key}][请求类型]不合法", QMessageBox.Yes,
                                         QMessageBox.Yes)
                    continue

            # 赋值
            res_detail[key] = {"url": url, "time": 0, "result": True, "detail": []}

            # 获取接口信息
            header = self.interface_dict[key]["header"]
            if isinstance(header, (dict, list)) and "cookie" in header:
                cookie = self.interface_dict[key]["header"]["cookie"]
                del self.interface_dict[key]["header"]["cookie"]
            else:
                cookie = None

            try:
                response = requests.request(request_type.lower(),
                                            url=url,
                                            params=self.interface_dict[key]["params"],
                                            json=self.interface_dict[key]["body"],
                                            headers=self.interface_dict[key]["header"],
                                            cookies=cookie,
                                            timeout=5)
            except Exception as e:
                res_detail[key]["result"] = False
                res_detail[key]["detail"].append(f"连接目标服务器出错{e}")
            else:
                # 获取Json信息
                try:
                    r_json = response.json()
                except Exception:
                    r_json = None

                # 多个断言判断
                locals_ = {"response": response, "content_json": r_json}
                for assert_info in self.interface_dict[key]["assertion"]:
                    self._assert_opt(res_detail[key], assert_info, locals_)

            # 计时结束
            time_end = time.time()
            res_detail[key]["time"] = (time_end - time_start) * 1000

            # 停止
            if self.stop_flag:
                break

            # 发射信号
            self.SIGNAL_DONE.emit(key, res_detail[key])

        return res_detail

    def _assert_opt(self, res_detail_key, fun: str, locals_):
        """ 执行断言, 判断是否成功 """
        try:
            res = self._exec_func(fun, locals_=locals_)
        except Exception as e:
            res_detail_key["result"] = False
            res_detail_key["detail"].append(f"断言{fun}[语法出错]:{e}")
        else:
            if not res:
                res_detail_key["result"] = False
                res_detail_key["detail"].append(f"断言{fun}[结果不符合预期]: {locals_['content_json']}")

    def _exec_func(self, func: str, globals_=globals(), locals_=None):
        """ 作用域下执行断言语句 """
        if locals_ is None:
            locals_ = {}
        exec(f"ret = {func}", globals_, locals_)
        return locals_["ret"]
