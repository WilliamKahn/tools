from PySide6.QtCore import QSize, QPropertyAnimation, QEasingCurve, Qt, QByteArray
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QPushButton


class MaterialSidebarButton(QPushButton):
    def __init__(self, icon_name, text, parent=None):
        super().__init__(parent)
        self.setCheckable(True)
        self.setText(text)
        self.setIcon(QIcon(f"./icons/{icon_name}.svg"))
        self.setIconSize(QSize(22, 22))
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setObjectName("menu-btn")
        self.setProperty("class", "menu-btn")

        # Configure sizes for expanded/collapsed states
        self._expanded_width = 220
        self._collapsed_width = 44  # Make it smaller to fit icons only
        self._icon_name = icon_name
        self._text = text

        # Animation for icon size change
        self._animation = QPropertyAnimation(self, QByteArray(b"iconSize"))
        self._animation.setDuration(150)
        self._animation.setEasingCurve(QEasingCurve.Type.OutCubic)

    def update_state(self, expanded):
        # Update button appearance based on sidebar state
        if expanded:
            self.setText(self._text)
            self.setToolTip("")
        else:
            self.setText("")
            self.setToolTip(self._text)

        # Add animation for width change
        anim = QPropertyAnimation(self, QByteArray(b"minimumWidth"))
        anim.setDuration(300)
        anim.setStartValue(self.width())
        anim.setEndValue(self._expanded_width if expanded else self._collapsed_width)
        anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        anim.start()

        # Also set maximum width to match minimum when collapsed
        max_anim = QPropertyAnimation(self, QByteArray(b"maximumWidth"))
        max_anim.setDuration(300)
        max_anim.setStartValue(self.width())
        max_anim.setEndValue(self._expanded_width if expanded else self._collapsed_width)
        max_anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        max_anim.start()