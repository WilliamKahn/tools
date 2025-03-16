from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QPalette, QColor
from PySide6.QtCore import Qt

class ThemeManager:
    @staticmethod
    def is_dark_mode(app):
        # Check if app is in dark mode based on text color
        palette = app.palette()
        text_color = palette.color(QPalette.WindowText)
        return text_color.lightness() > 127

    @staticmethod
    def set_dark_mode(app, dark_mode=True):
        palette = QPalette()

        if dark_mode:
            # Dark theme colors
            palette.setColor(QPalette.ColorRole.Window, QColor(33, 33, 33))
            palette.setColor(QPalette.ColorRole.WindowText, QColor(255, 255, 255))
            palette.setColor(QPalette.ColorRole.Base, QColor(45, 45, 45))
            palette.setColor(QPalette.ColorRole.AlternateBase, QColor(53, 53, 53))
            palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(33, 33, 33))
            palette.setColor(QPalette.ColorRole.ToolTipText, QColor(255, 255, 255))
            palette.setColor(QPalette.ColorRole.Text, QColor(255, 255, 255))
            palette.setColor(QPalette.ColorRole.Button, QColor(53, 53, 53))
            palette.setColor(QPalette.ColorRole.ButtonText, QColor(255, 255, 255))
            palette.setColor(QPalette.ColorRole.Link, QColor(42, 130, 218))
            palette.setColor(QPalette.ColorRole.Highlight, QColor(42, 130, 218))
            palette.setColor(QPalette.ColorRole.HighlightedText, QColor(255, 255, 255))
        else:
            # Light theme colors
            palette.setColor(QPalette.ColorRole.Window, QColor(240, 240, 240))
            palette.setColor(QPalette.ColorRole.WindowText, QColor(33, 33, 33))
            palette.setColor(QPalette.ColorRole.Base, QColor(255, 255, 255))
            palette.setColor(QPalette.ColorRole.AlternateBase, QColor(247, 247, 247))
            palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(255, 255, 255))
            palette.setColor(QPalette.ColorRole.ToolTipText, QColor(33, 33, 33))
            palette.setColor(QPalette.ColorRole.Text, QColor(33, 33, 33))
            palette.setColor(QPalette.ColorRole.Button, QColor(240, 240, 240))
            palette.setColor(QPalette.ColorRole.ButtonText, QColor(33, 33, 33))
            palette.setColor(QPalette.ColorRole.Link, QColor(25, 118, 210))
            palette.setColor(QPalette.ColorRole.Highlight, QColor(25, 118, 210))
            palette.setColor(QPalette.ColorRole.HighlightedText, QColor(255, 255, 255))

        app.setPalette(palette)

    @staticmethod
    def apply_stylesheet(app):
        is_dark = ThemeManager.is_dark_mode(app)

        # Material Design colors
        primary_color = "#1976D2"  # Blue 700
        accent_color = "#FF4081"   # Pink A200

        if is_dark:
            bg_color = "#212121"        # Grey 900
            surface_color = "#333333"   # Custom dark surface
            on_surface = "#FFFFFF"      # White text
            divider_color = "#424242"   # Grey 800
        else:
            bg_color = "#FAFAFA"        # Grey 50
            surface_color = "#FFFFFF"   # White
            on_surface = "#212121"      # Grey 900 text
            divider_color = "#E0E0E0"   # Grey 300

        return f"""
            QMainWindow {{
                background-color: {bg_color};
            }}
            
            QPushButton {{
                padding: 10px 16px;
            }}

            QWidget#sidebar {{
                background-color: {surface_color};
                border-right: 1px solid {divider_color};
            }}

            QLabel.sidebar-title {{
                color: {on_surface};
                font-size: 18px;
                font-weight: bold;
                padding: 16px 0;
            }}

            QPushButton.sidebar-button {{
                background-color: transparent;
                color: {on_surface};
                text-align: left;
                border: none;
                border-radius: 4px;
                padding: 12px 16px;
            }}

            QPushButton.sidebar-button:hover {{
                background-color: {primary_color}30;
            }}

            QPushButton.sidebar-button:checked {{
                background-color: {primary_color}50;
            }}

            QLabel#sidebar-button-text {{
                color: {on_surface};
                font-size: 14px;
            }}

            QFrame.content-card {{
                background-color: {surface_color};
                border-radius: 8px;
                margin: 8px;
            }}

            QLabel.title {{
                color: {on_surface};
                font-size: 16px;
                font-weight: bold;
            }}

            QLabel.body-text {{
                color: {on_surface};
                font-size: 14px;
            }}
        """