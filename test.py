import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QStackedWidget,
    QVBoxLayout, QHBoxLayout, QLabel, QFrame, QGraphicsDropShadowEffect
)
from PySide6.QtGui import QIcon, QFont, QColor
from PySide6.QtCore import QEvent

from sidebar import MaterialSidebarButton
from theme import ThemeManager


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


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Modern UI Example")
        self.resize(1100, 700)

        # Track theme state
        self.current_theme = None

        # Main layout
        central_widget = QWidget()
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Sidebar
        self.sidebar = QWidget()
        self.sidebar.setObjectName("sidebar")
        sidebar_layout = QVBoxLayout(self.sidebar)
        sidebar_layout.setContentsMargins(8, 16, 8, 16)
        sidebar_layout.setSpacing(4)

        # Toggle button
        # In MainWindow.__init__, change the toggle_btn setup:
        self.toggle_btn = QLabel("Sidebar")
        self.toggle_btn.setObjectName("sidebar-title")  # Add an object name
        self.toggle_btn.setProperty("class", "sidebar-title")  # Add a class
        sidebar_layout.addWidget(self.toggle_btn)
        sidebar_layout.addSpacing(10)

        # Menu buttons
        self.menu_buttons = []
        menu_items = [
            {"icon": "home", "text": "Dashboard", "content": "Overview of your system"},
            {"icon": "analytics", "text": "Analytics", "content": "Data visualization and insights"},
            {"icon": "settings", "text": "Settings", "content": "Configure your application"},
            {"icon": "account_circle", "text": "Profile", "content": "Manage your account"}
        ]

        for item in menu_items:
            btn = MaterialSidebarButton(item["icon"], item["text"])
            btn.clicked.connect(self.switch_page)
            self.menu_buttons.append(btn)
            sidebar_layout.addWidget(btn)

        sidebar_layout.addStretch()

        # Theme toggle button
        self.theme_btn = MaterialSidebarButton("dark_mode", "Toggle Theme")
        self.theme_btn.clicked.connect(self.apply_theme)
        self.menu_buttons.append(self.theme_btn)
        sidebar_layout.addWidget(self.theme_btn)

        # Content area
        self.content = QStackedWidget()

        # Create pages
        for idx, item in enumerate(menu_items):
            page = QWidget()
            page_layout = QVBoxLayout(page)
            page_layout.setContentsMargins(16, 16, 16, 16)

            # Add multiple cards for each page
            card1 = ContentCard(
                f"{item['text']} Overview",
                f"This is the main {item['text'].lower()} card. {item['content']}."
            )

            card2 = ContentCard(
                "Additional Information",
                "This card contains supplementary information related to this section."
            )

            page_layout.addWidget(card1)
            page_layout.addWidget(card2)
            page_layout.addStretch()

            self.content.addWidget(page)

        # Add widgets to main layout
        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(self.content, 1)

        self.setCentralWidget(central_widget)

        # Initialize state
        self.menu_expanded = True
        self.sidebar.setFixedWidth(240)
        self.menu_buttons[0].setChecked(True)
        self.content.setCurrentIndex(0)

        # Apply theme
        self.apply_theme()

        # Install event filter to watch for palette changes
        app = QApplication.instance()
        app.installEventFilter(self)

    def eventFilter(self, obj, event):
        # Watch for palette change events to update theme
        if event.type() == QEvent.PaletteChange:
            self.apply_theme()
        return super().eventFilter(obj, event)

    def apply_theme(self):
        app = QApplication.instance()
        is_dark = ThemeManager.is_dark_mode(app)
        # Only update if theme changed
        if self.current_theme != is_dark:
            self.current_theme = is_dark
            stylesheet = ThemeManager.apply_stylesheet(app)
            self.setStyleSheet(stylesheet)

            # Update theme button icon
            icon_name = "light_mode" if is_dark else "dark_mode"
            self.theme_btn.setIcon(QIcon(f":/icons/{icon_name}"))


    def switch_page(self):
        clicked_button = self.sender()
        if clicked_button == self.theme_btn:
            return

        index = self.menu_buttons.index(clicked_button)

        # Update button states
        for btn in self.menu_buttons:
            btn.setChecked(btn is clicked_button)

        # Switch page with a fade effect
        self.content.setCurrentIndex(index)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Set application-wide font (fixed the typo)
    app.setFont(QFont("Segue UI", 10))

    window = MainWindow()
    window.show()
    sys.exit(app.exec())