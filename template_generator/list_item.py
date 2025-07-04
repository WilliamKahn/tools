import os

from PySide6.QtWidgets import QWidget, QHBoxLayout, QFileDialog, QMessageBox, QDialog, \
    QVBoxLayout, QTextEdit, QPushButton, QTextEdit, QLabel, QFileDialog, QCheckBox, QLineEdit, QSizePolicy
from PySide6.QtCore import Qt


class ListItemWidget(QWidget):
    def __init__(self, file_path, parent=None):
        super().__init__(parent)
        self.file_path = file_path

        # 进一步增加控件高度，确保所有文字完整显示
        self.setFixedHeight(60)
        self.setMinimumWidth(800)  # 增加最小宽度

        layout = QHBoxLayout()
        layout.setContentsMargins(10, 8, 10, 8)  # 增加边距
        layout.setSpacing(12)  # 增加控件间距

        # Checkbox - 固定尺寸
        self.checkbox = QCheckBox()
        self.checkbox.setFixedSize(24, 24)
        layout.addWidget(self.checkbox, 0)

        # 按钮布局 - 给按钮更多空间和更大尺寸
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(8)

        self.module_button = QPushButton("Module")
        # 修复QSizePolicy的访问方式
        self.module_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.module_button.clicked.connect(self.select_folder)
        buttons_layout.addWidget(self.module_button)

        self.package_button = QPushButton("Package")
        # 修复QSizePolicy的访问方式
        self.package_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.package_button.clicked.connect(self.select_folder)
        buttons_layout.addWidget(self.package_button)

        layout.addLayout(buttons_layout, 0)

        # Alias输入框 - 增加宽度和高度
        self.alias_edit = QLineEdit()
        self.alias_edit.setPlaceholderText("Alias")
        self.alias_edit.setMinimumSize(150, 40)  # 增加输入框尺寸
        self.alias_edit.setMaximumSize(180, 40)
        layout.addWidget(self.alias_edit, 0)

        # 显示文本 - 占用剩余空间，优化文本显示
        self.display_text = QLabel(os.path.basename(file_path))
        self.display_text.setToolTip(file_path)  # 鼠标悬停显示完整路径
        self.display_text.setWordWrap(False)
        self.display_text.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

        # 设置文本选择和最小高度
        self.display_text.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        self.display_text.setMinimumHeight(40)
        self.display_text.setMaximumHeight(40)

        # 设置边距确保文本完全可见
        self.display_text.setContentsMargins(8, 0, 8, 0)

        # 移除可能冲突的内联样式，让全局主题接管
        self.display_text.setObjectName("display-text")

        layout.addWidget(self.display_text, 1)  # 伸展因子为1，占用剩余空间

        self.setLayout(layout)

    # Other methods remain the same...
    def select_folder(self):
        sender = self.sender()

        # Get project path from parent
        parent_widget = self.parent()
        while parent_widget and not hasattr(parent_widget, 'config_button'):
            parent_widget = parent_widget.parent()

        project_path = parent_widget.config_button.toolTip() if parent_widget else ""

        if sender == self.module_button:

            if not project_path:
                QMessageBox.warning(self, "Warning", "Please select a project path first")
                return

            # Open dialog with project path as starting point
            folder = QFileDialog.getExistingDirectory(self, "Select Module Folder", project_path)

            # Verify module is a subdirectory of project
            if folder:
                if not os.path.normpath(folder).startswith(os.path.normpath(project_path)):
                    QMessageBox.critical(self, "Error", "Module must be a subdirectory of the project")
                    return
                folder = folder.replace(project_path, "")
                self.module_button.setToolTip(folder)
                last_folder = os.path.basename(folder)
                self.module_button.setText(last_folder)
                # 讲道理这里应该是设置package_button的toolTip和text
                self.package_button.setToolTip("")
                self.package_button.setText("Package")

        elif sender == self.package_button:
            # For package button, only allow selecting subdirectories of module
            module_path = self.module_button.toolTip()
            if not module_path and not project_path:
                QMessageBox.warning(self, "Warning", "Please select a module directory first")
                return
            path = project_path
            if module_path:
                path += module_path

            if self.display_text.text().split('.')[1] == 'java':
                path += "/src/main/java"
            elif self.display_text.text().split('.')[1] == 'xml':
                path += "/src/main/resources"

            # Open dialog with module path as starting point
            folder = QFileDialog.getExistingDirectory(self, "Select Package Folder", path)
            # Verify the selected folder is a subdirectory of module_path
            if folder:
                if not os.path.normpath(folder).startswith(os.path.normpath(path)):
                    QMessageBox.critical(self, "Error", "Package must be a subdirectory of the selected module")
                    return
                folder = folder.replace(path, "")
                self.package_button.setToolTip(folder)
                last_folder = os.path.basename(folder)
                self.package_button.setText(last_folder)


class FileEditor(QDialog):
    def __init__(self, file_path, parent=None):
        super().__init__(parent)
        self.file_path = file_path
        self.setWindowTitle(f"Edit {os.path.basename(file_path)}")
        self.resize(500, 400)

        layout = QVBoxLayout()
        self.text_edit = QTextEdit()
        layout.addWidget(self.text_edit)

        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_file)
        layout.addWidget(self.save_button)

        self.setLayout(layout)
        self.load_file()

    def load_file(self):
        try:
            with open(self.file_path, 'r') as file:
                self.text_edit.setText(file.read())
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load file: {e}")

    def save_file(self):
        try:
            with open(self.file_path, 'w') as file:
                file.write(self.text_edit.toPlainText())
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save file: {e}")