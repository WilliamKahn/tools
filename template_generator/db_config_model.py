from PySide6.QtCore import QObject, Property, Signal


class DBConfigModel(QObject):
    # 定义数据变化的信号
    dataChanged = Signal(set)

    def __init__(self):
        super().__init__()
        self._data = {}

    # 使用Property装饰器定义属性，绑定getter和setter，并关联信号
    def get_data(self):
        return self._data

    def set_data(self, value):
        self._data = value
        self.dataChanged.emit(self._data.keys())  # 数据变化时触发信号

    def add_data(self, key, value):
        self._data[key] = value
        self.dataChanged.emit(self._data.keys())

    def del_data(self, key):
        del self._data[key]
        self.dataChanged.emit(self._data.keys())

    data = Property(dict, get_data, set_data, add_data, del_data, notify=dataChanged)
