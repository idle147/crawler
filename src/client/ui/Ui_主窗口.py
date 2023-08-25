from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1121, 679)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/img/运行.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setAutoFillBackground(True)
        MainWindow.setStyleSheet("QComboBox{\n"
                                 "  color:#1e222b;\n"
                                 "  padding: 1px 15px 1px 3px;\n"
                                 "  border:1px solid rgba(228,228,228,1);\n"
                                 "  border-radius:8;\n"
                                 "  font-family: Microsoft YaHei;\n"
                                 "  font-size: 14px;\n"
                                 "}\n"
                                 "\n"
                                 "QComboBox QAbstractItemView{    /*列表 */\n"
                                 "    margin-top: 8px;\n"
                                 "    margin-left: 6px;\n"
                                 "    margin-bottom: 6px;\n"
                                 "    margin-right: 6px;\n"
                                 "    background:rgba(255,255,255,1);\n"
                                 "    border:1px solid rgba(228,228,228,1);\n"
                                 "    border-radius:8px;\n"
                                 "    font-size:12px;\n"
                                 "    font-family: Microsoft YaHei;\n"
                                 "    outline: 0px;\n"
                                 "    color:#1e222b;\n"
                                 "    padding-left: 16px;\n"
                                 "    padding-top: 12px;\n"
                                 "    padding-bottom:12px;\n"
                                 "    \n"
                                 "  }\n"
                                 "\n"
                                 "QComboBox QScrollBar::vertical{ /*滑条 主体部分*/\n"
                                 "    width:6px;\n"
                                 "    background:rgb(255,255,255);\n"
                                 "    border:none;\n"
                                 "}\n"
                                 "QComboBox QScrollBar::handle::vertical{ /*滑块主体*/\n"
                                 "    border-radius:3px;\n"
                                 "    background-color: rgba(30, 34, 43, 0.2);\n"
                                 "}\n"
                                 "QComboBox QScrollBar::handle::vertical::hover{\n"
                                 "    background-color: rgba(30, 34, 43, 0.2);\n"
                                 "}\n"
                                 "\n"
                                 "QDialog {\n"
                                 "    background: #D6DBE9;\n"
                                 "}\n"
                                 "\n"
                                 "QLineEdit {\n"
                                 "    border: 1px solid #A0A0A0; /* 边框宽度为1px，颜色为#A0A0A0 */\n"
                                 "    border-radius: 3px; /* 边框圆角 */\n"
                                 "    padding-left: 5px; /* 文本距离左边界有5px */\n"
                                 "    background-color: #F2F2F2; /* 背景颜色 */\n"
                                 "    color: #A0A0A0; /* 文本颜色 */\n"
                                 "    selection-background-color: #A0A0A0; /* 选中文本的背景颜色 */\n"
                                 "    selection-color: #F2F2F2; /* 选中文本的颜色 */\n"
                                 "    font-family: \"Microsoft YaHei\"; /* 文本字体族 */\n"
                                 "    font-size: 10pt; /* 文本字体大小 */\n"
                                 "}\n"
                                 "\n"
                                 "QLineEdit:hover { /* 鼠标悬浮在QLineEdit时的状态 */\n"
                                 "    border: 1px solid #298DFF;\n"
                                 "    border-radius: 3px;\n"
                                 "    background-color: #F2F2F2;\n"
                                 "    color: #298DFF;\n"
                                 "    selection-background-color: #298DFF;\n"
                                 "    selection-color: #F2F2F2;\n"
                                 "}\n"
                                 "\n"
                                 "QLineEdit[echoMode=\"2\"] { /* QLineEdit有输入掩码时的状态 */\n"
                                 "    lineedit-password-character: 9679;\n"
                                 "    lineedit-password-mask-delay: 2000;\n"
                                 "}\n"
                                 "\n"
                                 "QLineEdit:disabled { /* QLineEdit在禁用时的状态 */\n"
                                 "    border: 1px solid #CDCDCD;\n"
                                 "    background-color: #CDCDCD;\n"
                                 "    color: #B4B4B4;\n"
                                 "}\n"
                                 "\n"
                                 "QLineEdit:read-only { /* QLineEdit在只读时的状态 */\n"
                                 "    background-color: #CDCDCD;\n"
                                 "    color: #F2F2F2;\n"
                                 "}")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 1131, 661))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(15)
        self.tabWidget.setFont(font)
        self.tabWidget.setStyleSheet("QTabWidget::tab-bar {\n"
                                     " background-color: black;\n"
                                     "}\n"
                                     "\n"
                                     "QTabBar::tab:!selected {\n"
                                     "    background-color: #9E9E9E;\n"
                                     "    color: white;\n"
                                     "}\n"
                                     "\n"
                                     "QTabWidget::pane { \n"
                                     "     position: absolute;\n"
                                     "}\n"
                                     "\n"
                                     "QTabBar::tab:selected {\n"
                                     "    border-color:#4094da;\n"
                                     "    background-color: #4094da;\n"
                                     "    color: white;\n"
                                     "}\n"
                                     "QTabBar::tab {\n"
                                     "     background: gray;\n"
                                     "     border: 2px solid #C4C4C3;\n"
                                     "     border-bottom-color: #C2C7CB;\n"
                                     "     border-top-left-radius: 4px;\n"
                                     "     border-top-right-radius: 4px;\n"
                                     "     min-width: 30px;\n"
                                     "     padding: 2px;\n"
                                     "}")
        self.tabWidget.setTabPosition(QtWidgets.QTabWidget.West)
        self.tabWidget.setObjectName("tabWidget")
        self.option = QtWidgets.QWidget()
        self.option.setObjectName("option")
        self.tree_view = QtWidgets.QTreeView(self.option)
        self.tree_view.setGeometry(QtCore.QRect(0, 0, 361, 649))
        self.tree_view.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.tree_view.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.tree_view.setObjectName("tree_view")
        self.gridLayoutWidget_3 = QtWidgets.QWidget(self.option)
        self.gridLayoutWidget_3.setGeometry(QtCore.QRect(363, 0, 711, 649))
        self.gridLayoutWidget_3.setObjectName("gridLayoutWidget_3")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.gridLayoutWidget_3)
        self.gridLayout_3.setContentsMargins(7, 7, 7, 7)
        self.gridLayout_3.setHorizontalSpacing(20)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label_assertion = QtWidgets.QLabel(self.gridLayoutWidget_3)
        self.label_assertion.setMaximumSize(QtCore.QSize(100, 16777215))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(12)
        self.label_assertion.setFont(font)
        self.label_assertion.setAlignment(QtCore.Qt.AlignCenter)
        self.label_assertion.setObjectName("label_assertion")
        self.gridLayout_3.addWidget(self.label_assertion, 6, 0, 1, 1)
        self.comboBox_type = QtWidgets.QComboBox(self.gridLayoutWidget_3)
        self.comboBox_type.setMinimumSize(QtCore.QSize(0, 30))
        self.comboBox_type.setMaximumSize(QtCore.QSize(16777215, 30))
        self.comboBox_type.setObjectName("comboBox_type")
        self.comboBox_type.addItem("")
        self.comboBox_type.addItem("")
        self.comboBox_type.addItem("")
        self.comboBox_type.addItem("")
        self.gridLayout_3.addWidget(self.comboBox_type, 1, 1, 1, 3)
        self.lineEdit_url = QtWidgets.QLineEdit(self.gridLayoutWidget_3)
        self.lineEdit_url.setMinimumSize(QtCore.QSize(0, 30))
        self.lineEdit_url.setMaximumSize(QtCore.QSize(16777215, 30))
        self.lineEdit_url.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft
                                       | QtCore.Qt.AlignTop)
        self.lineEdit_url.setObjectName("lineEdit_url")
        self.gridLayout_3.addWidget(self.lineEdit_url, 2, 1, 1, 3)
        self.comboBox_task = QtWidgets.QComboBox(self.gridLayoutWidget_3)
        self.comboBox_task.setMinimumSize(QtCore.QSize(0, 30))
        self.comboBox_task.setMaximumSize(QtCore.QSize(200, 30))
        self.comboBox_task.setObjectName("comboBox_task")
        self.gridLayout_3.addWidget(self.comboBox_task, 0, 3, 1, 1)
        self.textEdit_assert = QtWidgets.QTextEdit(self.gridLayoutWidget_3)
        self.textEdit_assert.setObjectName("textEdit_assert")
        self.gridLayout_3.addWidget(self.textEdit_assert, 6, 1, 1, 3)
        self.label_body = QtWidgets.QLabel(self.gridLayoutWidget_3)
        self.label_body.setMaximumSize(QtCore.QSize(100, 16777215))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(12)
        self.label_body.setFont(font)
        self.label_body.setAlignment(QtCore.Qt.AlignCenter)
        self.label_body.setObjectName("label_body")
        self.gridLayout_3.addWidget(self.label_body, 5, 0, 1, 1)
        self.textEdit_body = QtWidgets.QTextEdit(self.gridLayoutWidget_3)
        self.textEdit_body.setObjectName("textEdit_body")
        self.gridLayout_3.addWidget(self.textEdit_body, 5, 1, 1, 3)
        self.label_params = QtWidgets.QLabel(self.gridLayoutWidget_3)
        self.label_params.setMaximumSize(QtCore.QSize(100, 16777215))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(12)
        self.label_params.setFont(font)
        self.label_params.setAlignment(QtCore.Qt.AlignCenter)
        self.label_params.setObjectName("label_params")
        self.gridLayout_3.addWidget(self.label_params, 4, 0, 1, 1)
        self.label_interface = QtWidgets.QLabel(self.gridLayoutWidget_3)
        self.label_interface.setMaximumSize(QtCore.QSize(100, 16777215))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(12)
        self.label_interface.setFont(font)
        self.label_interface.setAlignment(QtCore.Qt.AlignCenter)
        self.label_interface.setObjectName("label_interface")
        self.gridLayout_3.addWidget(self.label_interface, 0, 0, 1, 1)
        self.label_header = QtWidgets.QLabel(self.gridLayoutWidget_3)
        self.label_header.setMaximumSize(QtCore.QSize(100, 16777215))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(12)
        self.label_header.setFont(font)
        self.label_header.setAlignment(QtCore.Qt.AlignCenter)
        self.label_header.setObjectName("label_header")
        self.gridLayout_3.addWidget(self.label_header, 3, 0, 1, 1)
        self.label_url = QtWidgets.QLabel(self.gridLayoutWidget_3)
        self.label_url.setMaximumSize(QtCore.QSize(100, 16777215))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(12)
        self.label_url.setFont(font)
        self.label_url.setAlignment(QtCore.Qt.AlignCenter)
        self.label_url.setObjectName("label_url")
        self.gridLayout_3.addWidget(self.label_url, 2, 0, 1, 1)
        self.label_task = QtWidgets.QLabel(self.gridLayoutWidget_3)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(12)
        self.label_task.setFont(font)
        self.label_task.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing
                                     | QtCore.Qt.AlignVCenter)
        self.label_task.setObjectName("label_task")
        self.gridLayout_3.addWidget(self.label_task, 0, 2, 1, 1)
        self.textEdit_header = QtWidgets.QTextEdit(self.gridLayoutWidget_3)
        self.textEdit_header.setObjectName("textEdit_header")
        self.gridLayout_3.addWidget(self.textEdit_header, 3, 1, 1, 3)
        self.lineEdit_interface = QtWidgets.QLineEdit(self.gridLayoutWidget_3)
        self.lineEdit_interface.setMinimumSize(QtCore.QSize(0, 30))
        self.lineEdit_interface.setMaximumSize(QtCore.QSize(16777215, 30))
        self.lineEdit_interface.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft
                                             | QtCore.Qt.AlignTop)
        self.lineEdit_interface.setObjectName("lineEdit_interface")
        self.gridLayout_3.addWidget(self.lineEdit_interface, 0, 1, 1, 1)
        self.textEdit_params = QtWidgets.QTextEdit(self.gridLayoutWidget_3)
        self.textEdit_params.setObjectName("textEdit_params")
        self.gridLayout_3.addWidget(self.textEdit_params, 4, 1, 1, 3)
        self.label_type = QtWidgets.QLabel(self.gridLayoutWidget_3)
        self.label_type.setMaximumSize(QtCore.QSize(100, 16777215))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(12)
        self.label_type.setFont(font)
        self.label_type.setAlignment(QtCore.Qt.AlignCenter)
        self.label_type.setObjectName("label_type")
        self.gridLayout_3.addWidget(self.label_type, 1, 0, 1, 1)
        self.btn_save = QtWidgets.QPushButton(self.gridLayoutWidget_3)
        self.btn_save.setMinimumSize(QtCore.QSize(0, 0))
        self.btn_save.setMaximumSize(QtCore.QSize(200, 50))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei")
        font.setPointSize(17)
        self.btn_save.setFont(font)
        self.btn_save.setStyleSheet(".QPushButton,\n"
                                    ".QToolButton {\n"
                                    "    background: #FFF;\n"
                                    "    border: 2px solid #DCDFE6;\n"
                                    "    color: #606266;\n"
                                    "    padding: 5px;\n"
                                    "    border-radius: 5px;\n"
                                    "}\n"
                                    "\n"
                                    ".QPushButton:hover,\n"
                                    ".QToolButton:hover {\n"
                                    "    color: #409EFF;\n"
                                    "    border-color: #c6e2ff;\n"
                                    "    background-color: #ecf5ff;\n"
                                    "}\n"
                                    "\n"
                                    ".QPushButton:pressed,\n"
                                    ".QToolButton:pressed {\n"
                                    "    color: #3a8ee6;\n"
                                    "    border-color: #3a8ee6;\n"
                                    "    outline: 0;\n"
                                    "}")
        self.btn_save.setObjectName("btn_save")
        self.gridLayout_3.addWidget(self.btn_save, 7, 3, 1, 1)
        self.gridLayout_3.setColumnStretch(0, 1)
        self.gridLayout_3.setColumnStretch(1, 2)
        self.gridLayout_3.setColumnStretch(3, 2)
        self.tabWidget.addTab(self.option, "")
        self.entry = QtWidgets.QWidget()
        self.entry.setStyleSheet("")
        self.entry.setObjectName("entry")
        self.gridLayoutWidget_4 = QtWidgets.QWidget(self.entry)
        self.gridLayoutWidget_4.setGeometry(QtCore.QRect(0, 0, 1061, 651))
        self.gridLayoutWidget_4.setObjectName("gridLayoutWidget_4")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.gridLayoutWidget_4)
        self.gridLayout_4.setContentsMargins(0, 30, 0, 10)
        self.gridLayout_4.setHorizontalSpacing(0)
        self.gridLayout_4.setVerticalSpacing(30)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.label_choose = QtWidgets.QLabel(self.gridLayoutWidget_4)
        self.label_choose.setMaximumSize(QtCore.QSize(200, 150))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(15)
        self.label_choose.setFont(font)
        self.label_choose.setAlignment(QtCore.Qt.AlignCenter)
        self.label_choose.setObjectName("label_choose")
        self.gridLayout_4.addWidget(self.label_choose, 0, 0, 1, 1)
        self.tableWidget = QtWidgets.QTableWidget(self.gridLayoutWidget_4)
        self.tableWidget.setMaximumSize(QtCore.QSize(1000, 16777215))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei")
        font.setPointSize(-1)
        self.tableWidget.setFont(font)
        self.tableWidget.setStyleSheet(
            "/*表格的一种美化方式*/\n"
            "QHeaderView\n"
            "{\n"
            "    background:transparent;\n"
            "}\n"
            "\n"
            "QHeaderView::section\n"
            "{\n"
            "    font-size:20px;\n"
            "    font-family:\"Microsoft YaHei\";\n"
            "    color:#FFFFFF;\n"
            "    background:#60669B;\n"
            "    border: 1px solid;\n"
            "    text-align:left;\n"
            "    min-height:49px;\n"
            "    max-height:49px;\n"
            "    margin-left:0px;\n"
            "    padding-left:0px;\n"
            "}\n"
            "\n"
            "QTableWidget\n"
            "{\n"
            "    background:#FFFFFF;\n"
            "    border: 1px solid;\n"
            "\n"
            "    font-size:20px;\n"
            "    font-family:\"Microsoft YaHei\";\n"
            "    color:#666666;\n"
            "}\n"
            "QTableWidget::item\n"
            "{\n"
            "    border-bottom:1px solid ;\n"
            "}\n"
            "\n"
            "QTableWidget::item::selected\n"
            "{\n"
            "    color:red;\n"
            "    background:#EFF4FF;\n"
            "}\n"
            "\n"
            "\n"
            "QScrollBar::handle:vertical\n"
            "{\n"
            "    background: rgba(255,255,255,20%);\n"
            "    border: 0px solid grey;\n"
            "    border-radius:3px;\n"
            "    width: 8px;\n"
            "}\n"
            "\n"
            "QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical\n"
            "{\n"
            "    background:rgba(255,255,255,10%);\n"
            "}\n"
            "\n"
            "\n"
            "QScollBar::add-line:vertical, QScrollBar::sub-line:vertical\n"
            "{\n"
            "    background:transparent;\n"
            "}")
        self.tableWidget.setFrameShape(QtWidgets.QFrame.Box)
        self.tableWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.tableWidget.setSizeAdjustPolicy(
            QtWidgets.QAbstractScrollArea.AdjustToContentsOnFirstShow)
        self.tableWidget.setAutoScrollMargin(16)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, item)
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(170)
        self.tableWidget.horizontalHeader().setMinimumSectionSize(50)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.verticalHeader().setCascadingSectionResizes(False)
        self.tableWidget.verticalHeader().setDefaultSectionSize(50)
        self.tableWidget.verticalHeader().setMinimumSectionSize(50)
        self.tableWidget.verticalHeader().setStretchLastSection(False)
        self.gridLayout_4.addWidget(self.tableWidget, 1, 0, 1, 3)
        self.btn_do = QtWidgets.QPushButton(self.gridLayoutWidget_4)
        self.btn_do.setMaximumSize(QtCore.QSize(200, 50))
        self.btn_do.setObjectName("btn_do")
        self.gridLayout_4.addWidget(self.btn_do, 0, 2, 1, 1)
        self.comboBox_task_list = QtWidgets.QComboBox(self.gridLayoutWidget_4)
        self.comboBox_task_list.setMaximumSize(QtCore.QSize(550, 150))
        self.comboBox_task_list.setObjectName("comboBox_task_list")
        self.gridLayout_4.addWidget(self.comboBox_task_list, 0, 1, 1, 1)
        self.gridLayout_4.setColumnStretch(0, 2)
        self.gridLayout_4.setColumnStretch(1, 10)
        self.gridLayout_4.setRowStretch(0, 1)
        self.gridLayout_4.setRowStretch(1, 5)
        self.tabWidget.addTab(self.entry, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1121, 26))
        self.menubar.setObjectName("menubar")
        self.menu_file = QtWidgets.QMenu(self.menubar)
        self.menu_file.setObjectName("menu_file")
        MainWindow.setMenuBar(self.menubar)
        self.action_delete = QtWidgets.QAction(MainWindow)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/img/删除.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_delete.setIcon(icon1)
        self.action_delete.setObjectName("action_delete")
        self.action_edit = QtWidgets.QAction(MainWindow)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/img/编辑.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_edit.setIcon(icon2)
        self.action_edit.setObjectName("action_edit")
        self.action_import = QtWidgets.QAction(MainWindow)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/img/导入.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_import.setIcon(icon3)
        self.action_import.setObjectName("action_import")
        self.action_outport = QtWidgets.QAction(MainWindow)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/img/导出.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_outport.setIcon(icon4)
        self.action_outport.setObjectName("action_outport")
        self.action_del_group = QtWidgets.QAction(MainWindow)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/img/删除组.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_del_group.setIcon(icon5)
        self.action_del_group.setObjectName("action_del_group")
        self.action_modified_group = QtWidgets.QAction(MainWindow)
        self.action_modified_group.setIcon(icon2)
        self.action_modified_group.setObjectName("action_modified_group")
        self.action_add_interface = QtWidgets.QAction(MainWindow)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/img/新增.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_add_interface.setIcon(icon6)
        self.action_add_interface.setObjectName("action_add_interface")
        self.action_add_group = QtWidgets.QAction(MainWindow)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(":/img/新增任务组.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_add_group.setIcon(icon7)
        self.action_add_group.setObjectName("action_add_group")
        self.menu_file.addAction(self.action_import)
        self.menu_file.addSeparator()
        self.menu_file.addAction(self.action_outport)
        self.menubar.addAction(self.menu_file.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "接口测试工具"))
        self.label_assertion.setText(_translate("MainWindow", "Assertion:"))
        self.comboBox_type.setItemText(0, _translate("MainWindow", "GET"))
        self.comboBox_type.setItemText(1, _translate("MainWindow", "PUT"))
        self.comboBox_type.setItemText(2, _translate("MainWindow", "POST"))
        self.comboBox_type.setItemText(3, _translate("MainWindow", "DELETE"))
        self.label_body.setText(_translate("MainWindow", "body:"))
        self.label_params.setText(_translate("MainWindow", "params:"))
        self.label_interface.setText(_translate("MainWindow", "接口名称:"))
        self.label_header.setText(_translate("MainWindow", "Header:"))
        self.label_url.setText(_translate("MainWindow", "URL:"))
        self.label_task.setText(_translate("MainWindow", "任务："))
        self.textEdit_header.setHtml(
            _translate(
                "MainWindow",
                "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                "p, li { white-space: pre-wrap; }\n"
                "</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
                "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"
            ))
        self.label_type.setText(_translate("MainWindow", "请求类型:"))
        self.btn_save.setText(_translate("MainWindow", "完成"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.option),
                                  _translate("MainWindow", "录入接口"))
        self.label_choose.setText(_translate("MainWindow", "选择任务"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "名称"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "链接"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "耗时"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "执行结果"))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "错误详情"))
        self.btn_do.setText(_translate("MainWindow", "执 行"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.entry),
                                  _translate("MainWindow", "执行测试"))
        self.menu_file.setTitle(_translate("MainWindow", "文件"))
        self.action_delete.setText(_translate("MainWindow", "删除接口"))
        self.action_delete.setShortcut(_translate("MainWindow", "Del"))
        self.action_edit.setText(_translate("MainWindow", "编辑接口"))
        self.action_edit.setShortcut(_translate("MainWindow", "Ins"))
        self.action_import.setText(_translate("MainWindow", "导入配置文件"))
        self.action_import.setToolTip(_translate("MainWindow", "导入配置文件"))
        self.action_import.setShortcut(_translate("MainWindow", "F1"))
        self.action_outport.setText(_translate("MainWindow", "导出配置文件"))
        self.action_outport.setShortcut(_translate("MainWindow", "F2"))
        self.action_del_group.setText(_translate("MainWindow", "删除任务组"))
        self.action_del_group.setToolTip(_translate("MainWindow", "删除任务组"))
        self.action_modified_group.setText(_translate("MainWindow", "修改任务组"))
        self.action_modified_group.setToolTip(_translate("MainWindow", "修改任务组"))
        self.action_add_interface.setText(_translate("MainWindow", "新增接口"))
        self.action_add_interface.setToolTip(_translate("MainWindow", "新增接口"))
        self.action_add_group.setText(_translate("MainWindow", "新增任务组"))


import resource_rc
