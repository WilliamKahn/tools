from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

class Page3(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        label = QLabel("This is Page 3")
        layout.addWidget(label)
        self.setLayout(layout)