from PySide6.QtGui import QColor
from PySide6.QtWidgets import QFrame, QGraphicsDropShadowEffect, QVBoxLayout, QLabel


class ContentCard(QFrame):
    def __init__(self, title, content, parent=None):
        super().__init__(parent)
        self.setObjectName("content-card")
        self.setProperty("class", "content-card")

        # Create drop shadow effect properly
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(10)
        shadow.setColor(QColor(0, 0, 0, 20))  # rgba(0, 0, 0, 0.08) equivalent
        shadow.setOffset(0, 2)
        self.setGraphicsEffect(shadow)

        # Layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)

        # Title
        title_label = QLabel(title)
        title_label.setObjectName("title")
        title_label.setProperty("class", "title")

        # Content
        content_label = QLabel(content)
        content_label.setObjectName("body-text")
        content_label.setProperty("class", "body-text")
        content_label.setWordWrap(True)

        layout.addWidget(title_label)
        layout.addWidget(content_label)
        layout.addStretch()