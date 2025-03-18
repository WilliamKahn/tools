import json
import os
import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QStackedWidget,
    QVBoxLayout, QHBoxLayout, QLabel
)
from PySide6.QtGui import QIcon, QFont
from PySide6.QtCore import QEvent
from demo.demo import Demo
from sidebar import MaterialSidebarButton
from sql_generator.layout import SqlGenerator
from template_generator.layout import TemplateGenerator
from theme import ThemeManager


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Modern UI Example")
        self.resize(1100, 700)

        self.demo = Demo()
        self.sql_generator = SqlGenerator()
        self.template_generator = TemplateGenerator()

        self.init_ui()
        self.load_data()

    def init_ui(self):
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
            {"icon": "demo", "text": "Dashboard", "content": self.demo},
            {"icon": "template_generator", "text": "SQL Generator", "content": self.sql_generator},
            {"icon": "template_generator", "text": "Template Generator", "content": self.template_generator},
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
        sidebar_layout.addWidget(self.theme_btn)

        # Content area
        self.content = QStackedWidget()

        # Create pages
        for idx, item in enumerate(menu_items):
            self.content.addWidget(item['content'])

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
        if event.type() == QEvent.Type.PaletteChange:
            # Only process if we're not already updating the theme
            if not hasattr(self, '_updating_theme') or not self._updating_theme:
                self._updating_theme = True
                self.apply_theme()
                self._updating_theme = False
        return super().eventFilter(obj, event)

    def apply_theme(self):
        app = QApplication.instance()
        is_dark = ThemeManager.is_dark_mode(app)

        # Toggle theme when the button is clicked
        if self.sender() == self.theme_btn:
            is_dark = not is_dark
            self._updating_theme = True
            ThemeManager.set_dark_mode(app, is_dark)
            self._updating_theme = False

        # Update current theme state
        self.current_theme = is_dark

        # Apply stylesheet
        stylesheet = ThemeManager.apply_stylesheet(app)
        self._updating_theme = True
        self.setStyleSheet(stylesheet)
        self._updating_theme = False

        # Update theme button icon and text
        icon_name = "light_mode" if is_dark else "dark_mode"
        self.theme_btn.setIcon(QIcon(f":/icons/{icon_name}"))
        self.theme_btn.setText("亮色模式" if is_dark else "暗色模式")


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

    def closeEvent(self, event):
        self.save_data()
        super().closeEvent(event)

    def save_data(self):
        # 收集特定生成器的状态
        data = {
            "sqlGenerator": self.sql_generator.serialize(),
            "templateGenerator": self.template_generator.serialize()
        }
        with open("app_state.json", "w") as f:
            json.dump(data, f)

    def load_data(self):
        """加载时恢复所有控件数据"""
        if os.path.exists("app_state.json"):
            with open("app_state.json", "r") as f:
                data = json.load(f)

        if "sqlGenerator" in data:
            self.sql_generator.deserialize(data["sqlGenerator"])
        if "templateGenerator" in data:
            self.template_generator.deserialize(data["templateGenerator"])


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Set application-wide font (fixed the typo)
    app.setFont(QFont("Segue UI", 10))

    window = MainWindow()
    window.show()
    sys.exit(app.exec())