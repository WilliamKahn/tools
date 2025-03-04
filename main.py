# demo.py
import sys
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication
from qfluentwidgets import NavigationItemPosition, FluentWindow, setTheme, Theme
from qfluentwidgets import FluentIcon as FIF
from pages.page2 import Page2
from pages.sql_generator import SqlGenerator


class Window(FluentWindow):
    def __init__(self):
        super().__init__()

        # create sub interface
        self.page = SqlGenerator(self)
        self.page2 = Page2()

        self.initNavigation()
        self.initWindow()

    def initNavigation(self):
        # add sub interface
        self.addSubInterface(self.page, FIF.HOME, '专注时段1')
        self.addSubInterface(self.page2, FIF.ACCEPT, '12312312')

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


if __name__ == '__main__':
    setTheme(Theme.DARK)

    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    w = Window()
    w.show()
    app.exec()