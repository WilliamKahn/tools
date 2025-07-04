import json
import os
import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QStackedWidget,
    QVBoxLayout, QHBoxLayout, QLabel
)
from PySide6.QtGui import QFont, QPalette
from demo.demo import Demo
from sidebar import MaterialSidebarButton
from sql_generator.layout import SqlGenerator
from template_generator.layout import TemplateGenerator
from qt_material import apply_stylesheet


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("工具集")
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
        sidebar_layout = QVBoxLayout(self.sidebar)
        sidebar_layout.setContentsMargins(8, 16, 8, 16)
        sidebar_layout.setSpacing(4)

        # Menu buttons
        self.menu_buttons = []
        self.content = QStackedWidget()
        menu_items = [
            {"icon": "home", "text": "Dashboard", "content": self.demo},
            {"icon": "sql_generator", "text": "SQL Generator", "content": self.sql_generator},
            {"icon": "template_generator", "text": "Template Generator", "content": self.template_generator},
        ]

        for item in menu_items:
            btn = MaterialSidebarButton(item["icon"], item["text"])
            self.content.addWidget(item['content'])
            btn.clicked.connect(self.switch_page)
            self.menu_buttons.append(btn)
            sidebar_layout.addWidget(btn)
        sidebar_layout.addStretch()

        # Add widgets to main layout
        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(self.content, 1)

        self.setCentralWidget(central_widget)

        # Initialize state
        self.menu_expanded = True
        self.sidebar.setFixedWidth(240)
        self.menu_buttons[0].setChecked(True)
        self.content.setCurrentIndex(0)

    def switch_page(self):
        clicked_button = self.sender()

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
            json.dump(data, f, ensure_ascii=False, indent=4)

    def load_data(self):
        """加载时恢复所有控件数据"""
        if os.path.exists("app_state.json"):
            with open("app_state.json", "r") as f:
                data = json.load(f)

        if "sqlGenerator" in data:
            self.sql_generator.deserialize(data["sqlGenerator"])
        if "templateGenerator" in data:
            self.template_generator.deserialize(data["templateGenerator"])


def is_dark_mode():
    # 获取应用程序的调色板
    palette = QApplication.palette()

    # 获取窗口背景色
    background_color = palette.color(QPalette.ColorRole.Window)

    # 计算颜色亮度（使用ITU-R BT.709亮度公式）
    brightness = (0.2126 * background_color.red() +
                  0.7152 * background_color.green() +
                  0.0722 * background_color.blue())

    # 如果亮度小于128（0-255范围），认为是暗色模式
    return brightness < 128


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Set application-wide font (fixed the typo)
    app.setFont(QFont("Segue UI", 10))

    window = MainWindow()
    #获取系统主题色 根据主题色切换主题
    if is_dark_mode():
        apply_stylesheet(app, theme='dark_teal.xml')
    else:
        apply_stylesheet(app, theme='light_blue.xml')
    window.show()
    sys.exit(app.exec())