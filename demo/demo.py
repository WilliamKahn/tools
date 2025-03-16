from PySide6.QtWidgets import QFrame, QVBoxLayout

from content_card import ContentCard


class Demo(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName('demo')
        self.initUI()

    def initUI(self):
        page_layout = QVBoxLayout()
        page_layout.setContentsMargins(16, 16, 16, 16)

        # Add multiple cards for each page
        card1 = ContentCard(
            f"Demo Overview",
            f"This is the main demo card."
        )

        card2 = ContentCard(
            "Additional Information",
            "This card contains supplementary information related to this section."
        )

        page_layout.addWidget(card1)
        page_layout.addWidget(card2)
        page_layout.addStretch()
        self.setLayout(page_layout)