from PyQt5.QtWidgets import QWidget, QStackedWidget, QVBoxLayout
import importlib

class Content(QWidget):
    def __init__(self, parent, pages):
        super().__init__(parent)
        self.pages = pages
        self.initUI()

    def initUI(self):
        self.stackedWidget = QStackedWidget()
        for page in self.pages:
            module = importlib.import_module(page['module'])
            page_class = getattr(module, page['class'])
            self.stackedWidget.addWidget(page_class())

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.stackedWidget)
        self.setLayout(self.layout)

    def display(self, index):
        self.stackedWidget.setCurrentIndex(index)