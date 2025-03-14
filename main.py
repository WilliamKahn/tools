# demo.py
import json
import os
import sys
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication
from qfluentwidgets import NavigationItemPosition, FluentWindow, setTheme, Theme
from qfluentwidgets import FluentIcon as FIF
from template_generator.layout import TemplateGenerator
from sql_generator.layout import SqlGenerator


class Window(FluentWindow):
    def __init__(self):
        super().__init__()

        # create sub interface
        self.sqlGenerator = SqlGenerator(self)
        self.templateGenerator = TemplateGenerator(self)

        self.initNavigation()
        self.initWindow()
        self.load_data()

    def initNavigation(self):
        # add sub interface
        self.addSubInterface(self.sqlGenerator, FIF.HOME, 'SQL生成器')
        self.addSubInterface(self.templateGenerator, FIF.ARROW_DOWN, '代码生成器')

        self.navigationInterface.addItem(
            routeKey='settingInterface',
            icon=FIF.SETTING,
            text='设置',
            position=NavigationItemPosition.BOTTOM,
        )

        self.navigationInterface.setExpandWidth(280)

    def initWindow(self):
        self.resize(900, 700)
        self.setWindowIcon(QIcon(':/qfluentwidgets/images/logo.png'))
        self.setWindowTitle('开发小工具')

        desktop = QApplication.screens()[0].availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)

    def closeEvent(self, event):
        self.save_data()
        super().closeEvent(event)


    def save_data(self):
        # 收集特定生成器的状态
        data = {
            "sqlGenerator": self.sqlGenerator.serialize(),
            "templateGenerator": self.templateGenerator.serialize()
        }
        with open("app_state.json", "w") as f:
            json.dump(data, f)

    def load_data(self):
        """加载时恢复所有控件数据"""
        if os.path.exists("app_state.json"):
            with open("app_state.json", "r") as f:
                data = json.load(f)

        if "sqlGenerator" in data:
            self.sqlGenerator.deserialize(data["sqlGenerator"])
        if "templateGenerator" in data:
            self.templateGenerator.deserialize(data["templateGenerator"])



if __name__ == '__main__':
    setTheme(Theme.DARK)

    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    w = Window()
    w.show()
    app.exec()