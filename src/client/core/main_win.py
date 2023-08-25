import io
import json
import os
import time

from PyQt5 import QtCore, QtGui, QtWidgets

from .config import DEFAULT_DICT, EXPORT_PATH, REQUEST_TYPE
from .interface_test_win import InterfaceTestWin
from .json_model import QJsonModel, QJsonTreeItem
from .ui_main import Ui_MainWindow


class MainWin(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self):
        super(MainWin, self).__init__()
        self.setupUi(self)
        self.model = QJsonModel()
        self.tree_view.setModel(self.model)
        self.document = {}
        self.lineEdit_interface.setPlaceholderText("任务组下右键->新增接口")
        self.lineEdit_interface.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)

        # 多线程接口测试清单
        self.interface_list = [0 for _ in range(4)]

        # 状态清空
        self.__clean_init()

        # 菜单信息初始化
        self.__menu_init()

        # 信号和槽
        self.action_import.triggered.connect(self._slot_read_document)  # 导入文件
        self.action_outport.triggered.connect(self._slot_save_document)  # 导出文件
        self.tree_view.clicked.connect(self._slot_tree_clicked)  # 左键点击
        self.tree_view.customContextMenuRequested.connect(self._slot_show_context_menu)  # 右键菜单
        self.comboBox_task.currentIndexChanged.connect(self._slot_change_tree_view)  # 改变treeView
        self.btn_save.clicked.connect(self._save_info)  # 保存信息
        self.btn_do.clicked.connect(self.interface_test)  # 执行接口测试
        self.tableWidget.itemChanged.connect(self.tableWidget.resizeRowsToContents)

    def __clean_init(self):
        """ 编辑框清空 """
        self.model.clear()
        self.comboBox_task_list.clear()
        self.comboBox_task.clear()
        self.__editor_clean()

    def __menu_init(self):
        """ 菜单初始化 """
        # 初始化
        self.root_menu = QtWidgets.QMenu(self)
        self.root_menu.addAction(self.action_add_group)
        self.group_menu = QtWidgets.QMenu(self)
        self.group_menu.addActions(
            [self.action_del_group, self.action_modified_group, self.action_add_interface])
        self.item_menu = QtWidgets.QMenu(self)
        self.item_menu.addActions([self.action_delete, self.action_edit])

        # 信号与槽
        self.action_add_group.triggered.connect(self._slot_add_group)  # 新增任务组
        self.action_del_group.triggered.connect(lambda: self._slot_delete_item(True))  # 删除任务组
        self.action_modified_group.triggered.connect(
            lambda: self._slot_modified_item(True))  # 修改任务组

        self.action_add_interface.triggered.connect(self._slot_add_interface)  # 新增接口
        self.action_delete.triggered.connect(lambda: self._slot_delete_item(False))  # 删除接口
        self.action_edit.triggered.connect(lambda: self._slot_modified_item(False))  # 编辑接口

    def _judge_dir(self):
        # 判断当前焦点的文件等级
        item = self.tree_view.currentIndex.internalPointer()
        father_item = self.tree_view.currentIndex.parent().internalPointer()
        grandfather_item = self.tree_view.currentIndex.parent().parent().internalPointer()
        if item is None:
            return 0
        if father_item is None:
            return 1
        elif grandfather_item is None:
            return 2
        else:
            return 3

    def _slot_add_group(self):
        """ 新增任务组 """
        # 弹出输入对话框
        info, ok = QtWidgets.QInputDialog.getText(self, "输入信息", "请输入任务组名字")
        if ok:
            # 任务组名字校验
            if info in self.document:
                QtWidgets.QMessageBox.critical(self, "新建任务组", "已存在该任务组", QtWidgets.QMessageBox.Yes,
                                               QtWidgets.QMessageBox.Yes)
            else:
                self.document[info] = {}
                self.model.insert_item(QtCore.QModelIndex(), key=info)
                self.comboBox_task.addItem(info)
                self.comboBox_task_list.addItem(info)

    def _slot_add_interface(self):
        """ 新增接口 """
        # 当前索引判断
        if self.tree_view.currentIndex is None:
            QtWidgets.QMessageBox.critical(self, "删除", "未选择索引", QtWidgets.QMessageBox.Yes,
                                           QtWidgets.QMessageBox.Yes)
            return
        key = self.tree_view.currentIndex.internalPointer().key
        # 弹出输入对话框
        info, ok = QtWidgets.QInputDialog.getText(self, "输入信息", "请输入新增接口名")
        if ok:
            # 接口名字校验
            if info in self.document[key]:
                QtWidgets.QMessageBox.critical(self, "新增接口", "已存在该接口", QtWidgets.QMessageBox.Yes,
                                               QtWidgets.QMessageBox.Yes)
            else:
                pos = self.model.insert_item(self.tree_view.currentIndex, key=info, **DEFAULT_DICT)
                self.document[key][info] = DEFAULT_DICT
                self.lineEdit_interface.setText(info)
                # treeview定位位置
                index = self.model.index(pos, 0, self.tree_view.currentIndex)
                self._tree_expand(index)

    def _slot_change_tree_view(self):
        # if self._judge_dir() == 2:
        #     res = QtWidgets.QMessageBox.information(
        #         self, "更改任务组", "是否更改任务组", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
        #         QtWidgets.QMessageBox.No)
        #     if res == QtWidgets.QMessageBox.Yes:
        #         QtWidgets.QMessageBox.information(self, "更改任务组", "该功能未实现, 请在对应任务组下右键->新增接口",
        #                                           QtWidgets.QMessageBox.No,
        #                                           QtWidgets.QMessageBox.No)
        self.lineEdit_interface.setText("")
        pos = self.comboBox_task.currentIndex()
        if self._judge_dir() == 1:
            index = self.model.index(pos, 0)
            self._tree_expand(index)

    def _tree_expand(self, index):
        """ tree定位指定的index """
        self.tree_view.setExpanded(self.tree_view.currentIndex, True)
        self.tree_view.setExpanded(index, True)
        self.tree_view.setCurrentIndex(index)
        self.tree_view.currentIndex = index

    def _slot_delete_item(self, is_first):
        """ 删除item """
        # 获取被删除的index属性
        item = self.tree_view.currentIndex.internalPointer()
        father_item = self.tree_view.currentIndex.parent().internalPointer()
        if item is None:
            QtWidgets.QMessageBox.critical(self, "删除", "未选择索引", QtWidgets.QMessageBox.Yes,
                                           QtWidgets.QMessageBox.Yes)
            return
        # 判断是否是删除根节点
        if is_first:
            del self.document[item.key]
            self.comboBox_task.removeItem(self.tree_view.currentIndex.row())
            self.comboBox_task_list.removeItem(self.tree_view.currentIndex.row())
        else:
            del self.document[father_item.key][item.key]
            self.lineEdit_interface.setText("")

        # 模型为空则清空
        if not self.document:
            self.model.clear()
            self.__clean_init()
        else:
            self.model.delete_item(self.tree_view.currentIndex.parent(), item)

    def _slot_modified_item(self, is_first):
        """ 修改item """
        # 参数校验
        if self.tree_view.currentIndex is None:
            QtWidgets.QMessageBox.critical(self, "修改", "未选择索引", QtWidgets.QMessageBox.Yes,
                                           QtWidgets.QMessageBox.Yes)

            return

        # 循环判断修改是否合法
        while True:
            if is_first:
                info, ok = QtWidgets.QInputDialog.getText(self, "输入信息", "请修改的任务组名字")
                if not ok or info not in self.document:
                    break
                QtWidgets.QMessageBox.critical(self, "修改任务组", "已存在该任务组的名称",
                                               QtWidgets.QMessageBox.Yes,
                                               QtWidgets.QMessageBox.Yes)

            else:
                info, ok = QtWidgets.QInputDialog.getText(self, "输入信息", "请修改的接口名字")
                text = self.model.data(self.tree_view.currentIndex)
                parent_text = self.model.data(self.tree_view.currentIndex.parent())
                if not ok or info not in self.document[parent_text][text]:
                    break
                QtWidgets.QMessageBox.critical(self, "修改接口", "任务组内已存在同名接口名称",
                                               QtWidgets.QMessageBox.Yes,
                                               QtWidgets.QMessageBox.Yes)
            continue

        # 更新
        if info != "" and ok:
            des_item = self.tree_view.currentIndex.internalPointer()
            # 更新document
            if is_first:
                self.document[info] = self.document.pop(des_item.key)
            else:
                self.document[parent_text][info] = self.document[parent_text].pop(des_item.key)
            # 更新model
            des_item.key = info
            pos = self.tree_view.currentIndex.row()
            # 更新控件
            if is_first:
                self.comboBox_task.removeItem(pos)
                self.comboBox_task_list.removeItem(pos)
                self.comboBox_task.insertItem(pos, info)
                self.comboBox_task_list.insertItem(pos, info)
            else:
                self.lineEdit_interface.setText(info)

    def _slot_read_document(self):
        """ 读取json文件 """
        replay = QtWidgets.QMessageBox.Yes
        if self.document:
            replay = QtWidgets.QMessageBox.warning(
                self, "文件导入", "当前列表不为空, 导入会覆盖现有数据,是否确定 ",
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)

        if replay == QtWidgets.QMessageBox.Yes:
            file_path = QtWidgets.QFileDialog.getOpenFileName(self, "打开文件", EXPORT_PATH,
                                                              "JSON文件(*.json)")[0]
            if not file_path:
                return
            with io.open(file_path, "r", encoding="utf8", errors="replace") as f:
                info = f.read()
            # 空文件检验
            if info == "":
                QtWidgets.QMessageBox.warning(self, "文件导入", "导入的文件为空", QtWidgets.QMessageBox.Yes,
                                              QtWidgets.QMessageBox.Yes)
                return
            try:
                self.__clean_init()
                self.document = json.loads(info)
                self.model.load(self.document)
            except Exception:
                QtWidgets.QMessageBox.critical(self, "文件导入", "文件导入失败", QtWidgets.QMessageBox.Yes,
                                               QtWidgets.QMessageBox.Yes)
            else:
                self.tree_view.currentIndex = self.model.index(0, 0)
                # 初始化任务列表项目
                self.comboBox_task.clear()
                self.comboBox_task_list.clear()
                for key in self.document:
                    self.comboBox_task.addItem(key)
                    self.comboBox_task_list.addItem(key)

    def _slot_save_document(self):
        """ 保存json文件 """
        if not self.document:
            QtWidgets.QMessageBox.warning(self, "文件保存", "无导出数据", QtWidgets.QMessageBox.Yes,
                                          QtWidgets.QMessageBox.Yes)
            return

        # 保存文件
        default_save_path = os.path.join(EXPORT_PATH, f"{int(time.time())}.json")
        if file_path := QtWidgets.QFileDialog.getSaveFileName(self, "保存文件", default_save_path,
                                                              "JSON文件(*.json)")[0]:
            if not file_path:
                return
            try:
                save_info = json.dumps(self.document, indent=4, ensure_ascii=False)
                with open(file_path, "w", encoding="utf8") as f:
                    f.write(save_info)
            except Exception:
                QtWidgets.QMessageBox.critical(self, "文件保存", "文件保存失败", QtWidgets.QMessageBox.Yes,
                                               QtWidgets.QMessageBox.Yes)
            else:
                QtWidgets.QMessageBox.information(self, "文件保存", "文件保存成功",
                                                  QtWidgets.QMessageBox.Yes,
                                                  QtWidgets.QMessageBox.Yes)

    def _slot_tree_clicked(self, model_index):
        self.tree_view.currentIndex = model_index
        index = self._judge_dir()
        if index == 1:
            self.__editor_clean()
            self.lineEdit_interface.setText("")
            self._task_assignment(model_index.internalPointer().key)
        elif index == 2:
            self.__controls_assignment(model_index)
        elif index == 3:
            self.__controls_assignment(model_index.parent())

    def __editor_clean(self):
        """ 清空编辑框的控件 """
        self.textEdit_header.setText("")
        self.textEdit_params.setText("")
        self.textEdit_body.setText("")
        self.lineEdit_url.setText("")
        self.textEdit_assert.setText("")

    def __controls_assignment(self, model_index):
        """ 控件赋值 """
        father_item = model_index.parent().internalPointer()
        res = self.model.json(model_index.internalPointer())
        self._type_assignment(res)
        self._task_assignment(father_item.key)
        self.lineEdit_interface.setText(model_index.internalPointer().key)
        self._lineedit_assignment(res, "URL", self.lineEdit_url)
        self._lineedit_assignment(res, "header", self.textEdit_header)
        self._lineedit_assignment(res, "params", self.textEdit_params)
        self._lineedit_assignment(res, "body", self.textEdit_body)
        self._lineedit_assignment(res, "assertion", self.textEdit_assert)

    def _slot_show_context_menu(self, pos):
        """ 创建右键菜单 """
        # 判断选择的节点
        self.tree_view.currentIndex = self.tree_view.indexAt(pos)

        # 未选中节点
        if self.tree_view.currentIndex.internalPointer() is None:
            # 将它移动到鼠标点击的位置, 并显示
            self.root_menu.popup(QtGui.QCursor.pos())
        # 一级目录
        elif self.tree_view.currentIndex.parent().internalPointer() is None:
            self.group_menu.popup(QtGui.QCursor.pos())
        # 二级条目
        elif self.tree_view.currentIndex.parent().parent().internalPointer() is None:
            self.item_menu.popup(QtGui.QCursor.pos())
        # 其他条目
        else:
            return

    def _lineedit_assignment(self, dict_info, key, lineedit):
        """ 字典参数判断 """
        # 参数校验
        info = ""
        if key not in dict_info:
            QtWidgets.QMessageBox.critical(self, "参数校验", f"缺少[{key}]字段", QtWidgets.QMessageBox.Yes,
                                           QtWidgets.QMessageBox.Yes)
        else:
            info = str(dict_info[key])

        # 标签赋值
        try:
            lineedit.setText(info)
        except Exception as e:
            print(e)

    def _type_assignment(self, dict_info):
        """ 请求类型校验 """
        # 参数校验
        if "请求类型" not in dict_info:
            QtWidgets.QMessageBox.critical(self, "参数校验", "缺少[请求类型]字段", QtWidgets.QMessageBox.Yes,
                                           QtWidgets.QMessageBox.Yes)
            return
        # 标签赋值
        key = dict_info["请求类型"]
        if key not in REQUEST_TYPE:
            QtWidgets.QMessageBox.critical(self, "参数校验", f"[请求类型]{key}内容错误",
                                           QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.Yes)
            return
        try:
            self.comboBox_type.setCurrentIndex(REQUEST_TYPE.index(key))
        except Exception as e:
            print(e)

    def _task_assignment(self, text):
        """ 控件赋值检查 """
        index = self.comboBox_task.findText(text)
        if index == -1:
            QtWidgets.QMessageBox.critical(self, "参数校验", f"查无该任务组{text}",
                                           QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.Yes)
        else:
            self.comboBox_task.setCurrentIndex(index)

    def _save_info(self):
        """ 保存当前控件的信息 """

        def json_analysis(info, control_name, to_change=True):
            if info != "":
                if to_change:
                    info = info.replace("\'", '\"')
                try:
                    json_info = json.loads(info)
                except Exception:
                    QtWidgets.QMessageBox.critical(self, "Json格式解析",
                                                   f"控件[{control_name}]的Json格式解析错误,请检查",
                                                   QtWidgets.QMessageBox.Yes,
                                                   QtWidgets.QMessageBox.Yes)
                    return 0
            else:
                return -1
            return json_info

        item = self.tree_view.currentIndex.internalPointer()
        father_item = self.tree_view.currentIndex.parent().internalPointer()
        grandfather_item = self.tree_view.currentIndex.parent().parent().internalPointer()

        # 一级索引无法保存
        if item is None \
            or father_item is None \
                or grandfather_item is not None \
                    or self.lineEdit_interface.text() == "":
            QtWidgets.QMessageBox.critical(self, "保存接口", "请选中要保存的接口条目", QtWidgets.QMessageBox.Yes,
                                           QtWidgets.QMessageBox.Yes)

            return

        # URL地址为空不能保存
        if self.lineEdit_url.text() == "":
            QtWidgets.QMessageBox.critical(self, "保存接口", "URL地址不能为空", QtWidgets.QMessageBox.Yes,
                                           QtWidgets.QMessageBox.Yes)

            return

        # 解析json
        header_info = json_analysis(self.textEdit_header.toPlainText(), "Header")
        params_info = json_analysis(self.textEdit_params.toPlainText(), "params_info")
        body_info = json_analysis(self.textEdit_body.toPlainText(), "body_info")

        # eval解析
        try:
            assert_info = eval(self.textEdit_assert.toPlainText())
        except Exception:
            QtWidgets.QMessageBox.critical(self, "解析assert_info", "解析失败",
                                           QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.Yes)
            return

        if header_info != 0 and params_info != 0 and body_info != 0:
            save_dict = {
                "URL": self.lineEdit_url.text(),
                "assertion": assert_info,
                "body": body_info if body_info != -1 else "",
                "header": header_info if header_info != -1 else "",
                "params": params_info if params_info != -1 else "",
                "请求类型": self.comboBox_type.currentText()
            }

            group_name = self.comboBox_task.currentText()
            self.document[group_name][self.lineEdit_interface.text()] = save_dict
            des_item = QJsonTreeItem.load(save_dict, father_item)
            des_item.key = self.lineEdit_interface.text()
            # 删除接口
            self.model.delete_item(self.tree_view.currentIndex.parent(), item)
            # 新增接口
            pos = self.model.insert_item(self.tree_view.currentIndex.parent(), des_item=des_item)
            new_index = self.model.index(pos, 0, self.tree_view.currentIndex.parent())
            # tree_view定位新增点
            self.tree_view.currentIndex = new_index
            self._tree_expand(self.tree_view.currentIndex)
            QtWidgets.QMessageBox.information(self, "保存接口", "接口保存成功", QtWidgets.QMessageBox.Yes,
                                              QtWidgets.QMessageBox.Yes)

    def interface_test(self):
        """ 启动接口测试 """
        if self.comboBox_task_list.currentText() != "":
            group_name = self.comboBox_task_list.currentText()
            # 判断是否有可以存储的list
            for pos, item in enumerate(self.interface_list):
                if item == 0:
                    # 实例化对象
                    interface_info = InterfaceTestWin(self.document[group_name], pos)
                    # 绑定
                    self.interface_list[pos] = interface_info
                    # 连接信号和槽
                    interface_info.GET_RES.connect(self.show_interface_data)
                    # 显示与启动线程
                    interface_info.show()
                    interface_info.thread_to_start()
                    break
            else:
                QtWidgets.QMessageBox.information(self, "接口测试", "接口测试窗口超过设置的线程上限",
                                                  QtWidgets.QMessageBox.Yes,
                                                  QtWidgets.QMessageBox.Yes)
        else:
            QtWidgets.QMessageBox.information(self, "接口测试", "未选择接口测试方案", QtWidgets.QMessageBox.Yes,
                                              QtWidgets.QMessageBox.Yes)

    def show_interface_data(self, key: str, res: dict, is_end: int):
        """ 写入tableWidget """
        if key and res:
            detail = "".join(info + "\n" for info in res["detail"])
            content_list = [
                key, res["url"], f"{res['time']:.2f}ms", "通过" if res["result"] else "异常", detail
            ]
            row_count = self.tableWidget.rowCount()
            self.tableWidget.insertRow(row_count)
            for pos, content in enumerate(content_list):
                self.tableWidget.setItem(row_count, pos, QtWidgets.QTableWidgetItem(content))

        if is_end != -1:
            self.interface_list[is_end] = 0
