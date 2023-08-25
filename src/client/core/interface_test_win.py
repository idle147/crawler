import copy

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMessageBox, QWidget

from .run_thread import SubThread
from .ui_dialog import Ui_Dialog


class InterfaceTestWin(QWidget, Ui_Dialog):
    # 自定义信号
    GET_RES = pyqtSignal(str, dict, int)
    STOP_THREAD = pyqtSignal()  # 定义关闭子线程的信号

    def __init__(self, interface_dict, index, parent=None):
        self.__globals__ = {}
        self.__locals__ = self.__globals__

        # 参数初始化
        self.index = index
        self.interface_dict = copy.deepcopy(interface_dict)
        self.total_len = len(interface_dict)
        self.quantity_finished = 0  # 完成数量

        # 窗口初始化
        super(InterfaceTestWin, self).__init__(parent)
        self.setupUi(self)
        self.label_process.setText(f"0/{self.total_len}")
        self.progressBar.setValue(0)
        self.progressBar.setRange(0, 100)

    def thread_to_start(self):
        # 初始化线程
        self.sub_thread = SubThread(self.interface_dict, self)
        self.sub_thread.SIGNAL_DONE.connect(self.update_progress)
        self.sub_thread.start()
        self.sub_thread.exec()

    def closeEvent(self, event):
        # 停止线程
        self.STOP_THREAD.emit()
        self.GET_RES.emit("", {}, self.index)

    def update_progress(self, key_info, dict_info):
        """ 更新进度条 """
        self.quantity_finished += 1
        res = f"{self.quantity_finished}/{self.total_len}"
        self.label_process.setText(res)
        value = eval(res) * 100
        self.progressBar.setValue(value)
        if value == 100:
            self.GET_RES.emit(key_info, dict_info, self.index)
            QMessageBox.information(self, "接口测试", "接口测试完成", QMessageBox.Yes, QMessageBox.Yes)
        else:
            self.GET_RES.emit(key_info, dict_info, -1)
