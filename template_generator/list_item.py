import os

from PySide6.QtWidgets import QWidget, QHBoxLayout, QFileDialog, QMessageBox, QDialog, \
    QVBoxLayout, QTextEdit, QPushButton, QTextEdit, QLabel, QFileDialog, QCheckBox, QLineEdit


class ListItemWidget(QWidget):
    def __init__(self, file_path, parent=None):
        super().__init__(parent)
        self.file_path = file_path

        # Set a reasonable fixed height for the widget
        self.setFixedHeight(40)

        layout = QHBoxLayout()
        layout.setContentsMargins(5, 2, 5, 2)  # Reduce margins
        layout.setSpacing(8)  # Add spacing between elements

        # Checkbox takes minimal space
        self.checkbox = QCheckBox()
        layout.addWidget(self.checkbox, 0)

        # Group module and package buttons in a separate layout to save space
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(2)

        self.module_button = QPushButton("Module")
        self.module_button.clicked.connect(self.select_folder)
        buttons_layout.addWidget(self.module_button)

        self.package_button = QPushButton("Package")
        self.package_button.clicked.connect(self.select_folder)
        buttons_layout.addWidget(self.package_button)

        layout.addLayout(buttons_layout, 1)

        # Alias edit with fixed width
        self.alias_edit = QLineEdit()
        self.alias_edit.setPlaceholderText("Alias")
        self.alias_edit.setFixedWidth(100)
        layout.addWidget(self.alias_edit, 0)

        # Display text takes all available space
        self.display_text = QLabel(os.path.basename(file_path))
        self.display_text.setToolTip(file_path)  # Show full path on hover
        self.display_text.setWordWrap(False)
        layout.addWidget(self.display_text, 1)  # Give stretch factor 1

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
        self.resize(400, 300)

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