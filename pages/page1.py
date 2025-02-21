import markdown
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTextEdit

class Page1(QWidget):
    def __init__(self):
        super().__init__()
        self.md_content = ""  # Initialize md_content
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.textEdit = QTextEdit()
        layout.addWidget(self.textEdit)
        self.setLayout(layout)
        self.textEdit.focusInEvent = self.focusInEvent
        self.textEdit.focusOutEvent = self.focusOutEvent

    def focusInEvent(self, event):
        self.textEdit.blockSignals(True)
        self.textEdit.setPlainText(self.md_content)
        self.textEdit.blockSignals(False)
        super(QTextEdit, self.textEdit).focusInEvent(event)

    def focusOutEvent(self, event):
        self.md_content = self.textEdit.toPlainText()
        html_content = markdown.markdown(self.md_content)
        self.textEdit.blockSignals(True)
        self.textEdit.setHtml(html_content)
        self.textEdit.blockSignals(False)
        super(QTextEdit, self.textEdit).focusOutEvent(event)