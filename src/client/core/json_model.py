from PyQt5 import QtCore


class QJsonTreeItem(object):

    def __init__(self, parent=None, key="", value=None):
        # 节点关系
        self._parent = parent
        self._children = []
        # Json的 key-value
        self._key = key
        self._value = value
        self._type = None
        # 超类调用
        super().__init__()

    def append_child(self, item):
        self._children.append(item)

    def delete_child(self, pos):
        self._children.pop(pos)

    def child_pos(self, item):
        return -1 if item not in self._children else self._children.index(item)

    def child(self, row):
        return self._children[row]

    def childCount(self):
        return len(self._children)

    def row(self):
        return (self._parent._children.index(self) if self._parent else 0)

    @property
    def children(self):
        return self._children

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, item):
        self._parent = item

    @property
    def key(self):
        return self._key

    @key.setter
    def key(self, key):
        self._key = key

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, typ):
        self._type = typ

    @classmethod
    def load(cls, value, parent_item=None, sort=False):
        # 初始化根节点
        root_item = QJsonTreeItem(parent_item)
        root_item.key = parent_item.key if parent_item is not None else "root"
        root_item.type = parent_item.type if parent_item is not None else None  # 递归生成字典属性子节点的数据
        if isinstance(value, dict):
            items = (sorted(value.items()) if sort else value.items())

            for key, value in items:
                child = cls.load(value, root_item)
                child.key = key
                child.type = type(value)
                root_item.append_child(child)
        # 递归生成list子节点信息
        elif isinstance(value, list):
            for index, value in enumerate(value):
                child = cls.load(value, root_item)
                child.key = index
                child.type = type(value)
                root_item.append_child(child)
        # 不包含父子关系
        else:
            root_item.value = value
            root_item.type = type(value)

        return root_item


class QJsonModel(QtCore.QAbstractItemModel):

    def __init__(self, parent=None):
        super(QJsonModel, self).__init__(parent)

        self._root_item = QJsonTreeItem()
        self._headers = ("条目", "属性")

    @property
    def root_item(self):
        return self._root_item

    def clear(self):
        self.load({})

    def load(self, document, sort=False):
        """Load from dictionary
        Arguments:
            document (dict): JSON-compatible dictionary
        """

        assert isinstance(document, (dict, list, tuple)), ("`document` 必须是 dict, list, tuple, "
                                                           "而不是 %s" % type(document))

        self.beginResetModel()

        self._root_item = QJsonTreeItem.load(document, sort=sort)
        self._root_item.type = type(document)

        self.endResetModel()

        return True

    def json(self, root=None):
        """ Serialization model as JSON-compliant dictionary
        Arguments:
            root (QJsonTreeItem, optional): 开始序列化, 默认为顶级项
        Returns:
            model(dict)
        """
        root = root or self._root_item
        return self.generate_json(root)

    def data(self, index, role=QtCore.Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return None

        item = index.internalPointer()

        if role == QtCore.Qt.ItemDataRole.DisplayRole:
            if index.column() == 0:
                return item.key

            if index.column() == 1:
                return item.value

        elif role == QtCore.Qt.ItemDataRole.EditRole:
            if index.column() == 1:
                return item.value

    def setData(self, index, value, role=QtCore.Qt.ItemDataRole.EditRole):
        self.dataChanged.emit(index, index)
        return True

    def headerData(self, section, orientation, role):
        if role != QtCore.Qt.ItemDataRole.DisplayRole:
            return None

        if orientation == QtCore.Qt.Orientation.Horizontal:
            return self._headers[section]

    def index(self, row, column, parent=QtCore.QModelIndex()):
        # 判断是不是一个有效的索引
        if not self.hasIndex(row, column, parent):
            return QtCore.QModelIndex()

        # 创建相应的索引
        parent_item = parent.internalPointer() if parent.isValid() else self._root_item
        if child_item := parent_item.child(row):
            return self.createIndex(row, column, child_item)
        else:
            return QtCore.QModelIndex()

    def parent(self, index):
        if not index.isValid():
            return QtCore.QModelIndex()

        child_item = index.internalPointer()
        parent_item = child_item.parent

        if parent_item == self._root_item:
            return QtCore.QModelIndex()

        return self.createIndex(parent_item.row(), 0, parent_item)

    def rowCount(self, parent=QtCore.QModelIndex()):
        if parent.column() > 0:
            return 0
        parent_item = parent.internalPointer() if parent.isValid() else self._root_item
        return parent_item.childCount()

    def columnCount(self, parent=QtCore.QModelIndex()):
        return 2

    def generate_json(self, item):
        n_child = item.childCount()
        if item.type is dict:
            document = {}
            for i in range(n_child):
                ch = item.child(i)
                document[ch.key] = self.generate_json(ch)
            return document

        elif item.type == list:
            document = []
            for i in range(n_child):
                ch = item.child(i)
                document.append(self.generate_json(ch))
            return document
        else:
            return item.value

    def insert_root_item(self, group_name):
        pos = self._root_item.childCount()
        self.beginInsertRows(QtCore.QModelIndex(), pos, pos + 1)
        group_item = QJsonTreeItem(self._root_item, key=group_name)
        self._root_item.append_child(group_item)
        self.endInsertRows()

    def insert_item(self, src_index: QtCore.QModelIndex, des_item=None, key=None, **kwargs):
        """ 插入单个item """
        # 数据初始化
        item = src_index.internalPointer()
        if item is None:
            item = self._root_item
        pos = item.childCount()

        # 参数校验
        if key is not None:
            des_item = QJsonTreeItem.load(value=kwargs, parent_item=item)
            des_item.key = key
            des_item.type = dict
            des_item.parent = item
        elif des_item is not None:
            des_item = des_item
        else:
            return -1

        # 插入组件
        self.beginInsertRows(src_index, pos, pos)
        item.append_child(des_item)
        self.endInsertRows()
        return pos

    def delete_item(self, src_index: QtCore.QModelIndex, des_item: QJsonTreeItem):
        """ 插入单个item """
        src_item = src_index.internalPointer()
        if src_item is None:
            src_item = self._root_item

        pos = src_item.child_pos(des_item)
        if pos == -1:
            return
        # 删除
        self.beginRemoveRows(src_index, pos, pos)
        src_item.delete_child(pos)
        self.endRemoveRows()
        return pos

    def modified_item(self, src_index, des_item):
        # 先删除
        self.delete_item(src_index, des_item)
        # 后增加
        return self.insert_item(src_index, des_item=des_item)
