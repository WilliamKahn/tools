from PyQt5.QtWidgets import QWidget, QVBoxLayout, QListWidget, QPushButton
import config

class Sidebar(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.expanded = True
        self.initUI()

    def initUI(self):
        self.listWidget = QListWidget()
        self.listWidget.addItems([page['name'] for page in config.pages])
        self.listWidget.currentRowChanged.connect(self.parent().switchContent)

        self.toggleButton = QPushButton("Toggle Menu")
        self.toggleButton.clicked.connect(self.toggleMenu)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.toggleButton)
        self.layout.addWidget(self.listWidget)

        self.setLayout(self.layout)
        self.setFixedWidth(150)

    def toggleMenu(self):
        if self.expanded:
            self.setFixedWidth(50)  # Partially hide the menu
            for i in range(self.listWidget.count()):
                item = self.listWidget.item(i)
                item.setText('')  # Hide text
        else:
            self.setFixedWidth(150)  # Expand the menu
            for i in range(self.listWidget.count()):
                item = self.listWidget.item(i)
                item.setText(config.pages[i]['name'])  # Show text
        self.expanded = not self.expanded