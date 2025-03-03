from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame

class Page2(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName('Page2')
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        label = QLabel("This is Page 2")
        layout.addWidget(label)
        self.setLayout(layout)