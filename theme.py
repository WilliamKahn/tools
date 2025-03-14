from PySide6.QtGui import QPalette


class ThemeManager:
    """Manages light and dark theme color schemes"""

    @staticmethod
    def is_dark_mode(app):
        # Get window color to determine if we're in dark mode
        window_color = app.palette().color(QPalette.ColorRole.Window)
        return window_color.lightness() < 128

    @staticmethod
    def get_theme_colors(app):
        is_dark = ThemeManager.is_dark_mode(app)

        if is_dark:
            return {
                "window_bg": "#121212",
                "sidebar_bg": "#1E1E1E",
                "card_bg": "#2D2D2D",
                "primary": "#90CAF9",
                "text_primary": "#FFFFFF",
                "text_secondary": "#B0B0B0",
                "hover": "#3A3A3A",
                "selected": "#263238",
                "border": "#333333",
                "divider": "#333333",
                "shadow": "rgba(0,0,0,0.3)"
            }
        else:
            return {
                "window_bg": "#F5F5F5",
                "sidebar_bg": "#FFFFFF",
                "card_bg": "#FFFFFF",
                "primary": "#2196F3",
                "text_primary": "#212121",
                "text_secondary": "#757575",
                "hover": "#E8EAF6",
                "selected": "#E3F2FD",
                "border": "#E0E0E0",
                "divider": "#EEEEEE",
                "shadow": "rgba(0,0,0,0.1)"
            }

    @staticmethod
    def apply_stylesheet(app):
        colors = ThemeManager.get_theme_colors(app)

        return f"""
            /* Main Window */
            QMainWindow {{
                background-color: {colors['window_bg']};
            }}

            /* Sidebar */
            #sidebar {{
                background-color: {colors['sidebar_bg']};
                border-right: 1px solid {colors['border']};
            }}
            
            /* Sidebar Title */
            #sidebar-title {{
                color: {colors['text_primary']};
                font-size: 18px;
                font-weight: bold;
                padding: 8px;
                margin-bottom: 8px;
            }}

            /* Content Area */
            QStackedWidget {{
                background-color: {colors['window_bg']};
            }}

            /* Toggle Button */
            #toggle_btn {{
                background-color: transparent;
                border: none;
                padding: 8px;
                border-radius: 18px;
                margin: 8px;
            }}
            #toggle_btn:hover {{
                background-color: {colors['hover']};
            }}
            #toggle_btn:pressed {{
                background-color: {colors['selected']};
            }}

            /* Menu Buttons */
            .menu-btn {{
                background-color: transparent;
                color: {colors['text_primary']};
                text-align: left;
                padding: 12px 16px;
                border: none;
                border-radius: 24px;
                margin: 4px 8px;
                font-weight: 500;
                font-size: 14px;
            }}
            .menu-btn:hover {{
                background-color: {colors['hover']};
            }}
            .menu-btn:checked {{
                background-color: {colors['selected']};
                color: {colors['primary']};
            }}

            /* Content Cards */
            .content-card {{
                background-color: {colors['card_bg']};
                border-radius: 12px;
                padding: 20px;
                margin: 16px;
            }}

            /* Typography */
            .title {{
                font-size: 22px;
                font-weight: 500;
                color: {colors['text_primary']};
                margin-bottom: 8px;
            }}

            .body-text {{
                font-size: 14px;
                color: {colors['text_secondary']};
                line-height: 1.5;
            }}
        """