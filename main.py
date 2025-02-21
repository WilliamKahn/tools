import sys
import config
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout
from sidebar import Sidebar
from content import Content

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.sidebar = Sidebar(self)
        self.content = Content(self, config.pages)

        self.layout = QHBoxLayout()
        self.layout.addWidget(self.sidebar)
        self.layout.addWidget(self.content)

        self.layout.setContentsMargins(0,0,0,0)
        self.layout.setSpacing(0)

        self.setLayout(self.layout)
        self.setWindowTitle('PyQt Example')
        self.setGeometry(300, 300, 800, 600)

    def switchContent(self, index):
        self.content.display(index)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())