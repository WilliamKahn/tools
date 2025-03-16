from lib2to3.fixes.fix_input import context

from PySide6.QtGui import QAction
from PySide6.QtWidgets import (QVBoxLayout, QHBoxLayout, QLabel, QFormLayout,
                               QSplitter, QWidget, QDialog, QListWidget, QLineEdit, QPushButton, QMenu, QMessageBox)
from PySide6.QtCore import Qt, Signal

class DatabaseConfigDialog(QDialog):

    def __init__(self, db_config):
        super().__init__()
        self.db_config = db_config
        self.current_config = None
        self.setWindowTitle("Database Configuration")
        self.resize(700, 400)
        self.initUI()

    def initUI(self):
        layout = QHBoxLayout(self)

        # Create a splitter for left and right panes
        splitter = QSplitter()

        # Left side: database config list
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)

        self.config_list = QListWidget()
        self.config_list.currentRowChanged.connect(self.on_config_selected)
        self.config_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.config_list.customContextMenuRequested.connect(self.show_context_menu)

        left_layout.addWidget(QLabel("Database Configurations:"))
        left_layout.addWidget(self.config_list)

        # Right side: configuration form
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)

        form_layout = QFormLayout()

        self.name_edit = QLineEdit()
        form_layout.addRow("Name:", self.name_edit)

        self.url_edit = QLineEdit()
        form_layout.addRow("URL:", self.url_edit)

        self.user_edit = QLineEdit()
        form_layout.addRow("Username:", self.user_edit)

        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.EchoMode.Password)
        form_layout.addRow("Password:", self.password_edit)

        self.port_edit = QLineEdit()
        form_layout.addRow("Port:", self.port_edit)

        right_layout.addLayout(form_layout)

        # Action buttons
        buttons_layout = QHBoxLayout()
        self.test_button = QPushButton("Test Connection")
        self.test_button.clicked.connect(self.test_connection)

        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_config)

        buttons_layout.addWidget(self.test_button)
        buttons_layout.addWidget(self.save_button)
        right_layout.addLayout(buttons_layout)

        # Add widgets to splitter
        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)
        splitter.setSizes([200, 500])

        layout.addWidget(splitter)

        # Initialize with config data
        self.load_config_list()

    def load_config_list(self):
        self.config_list.clear()
        self.config_list.addItems(self.db_config.get_data().keys())

    def on_config_selected(self, index):
        if index >= 0 and self.config_list.count() > 0:
            name = self.config_list.item(index).text()
            self.current_config = name
            config = self.db_config.get_data().get(name, {})
            self.name_edit.setText(name)
            self.url_edit.setText(config.get("host", ""))
            self.user_edit.setText(config.get("user", ""))
            self.password_edit.setText(config.get("password", ""))
            self.port_edit.setText(str(config.get("port")))

    def show_context_menu(self, position):
        if self.config_list.count() == 0:
            return

        menu = QMenu()
        action = QAction(text="Delete")
        action.triggered.connect(self.delete_config)
        menu.addAction(action)

        menu.exec_(self.config_list.mapToGlobal(position))

    def delete_config(self):
        current_item = self.config_list.currentItem()
        if not current_item:
            return

        name = current_item.text()

        # Use MessageBox instead of QMessageBox for a more consistent UI
        dialog = QMessageBox(
            "Confirm Delete",
            f"Are you sure you want to delete '{name}'?",
            self
        )

        dialog.yesButton.setText("Delete")
        dialog.cancelButton.setText("Cancel")

        if dialog.exec():
            self.db_config.del_data(name)
            self.load_config_list()
            self.clear_form()

    def clear_form(self):
        self.current_config = None
        self.name_edit.clear()
        self.url_edit.clear()
        self.user_edit.clear()
        self.password_edit.clear()
        self.port_edit.clear()

    def save_config(self):
        name = self.name_edit.text().strip()
        if not name:
            QMessageBox("Validation Error", "Please enter a name for this configuration", self).exec()
            return

        # Check if name already exists
        if name in self.db_config.get_data().keys():
            # Generate a unique name by adding a suffix
            base_name = name
            counter = 1
            while name in self.db_config.get_data().keys():
                name = f"{base_name}_{counter}"
                counter += 1

        # Collect current form data
        config = {
            "host": self.url_edit.text(),
            "user": self.user_edit.text(),
            "password": self.password_edit.text(),
            "port": int(self.port_edit.text())
        }

        # Always save as a new configuration
        self.db_config.add_data(name, config)

        # Set the current config to the new name
        self.current_config = name
        self.name_edit.setText(name)

        # Refresh the list
        self.load_config_list()

        # Select the newly saved item
        for i in range(self.config_list.count()):
            if self.config_list.item(i).text() == name:
                self.config_list.setCurrentRow(i)
                break

    def test_connection(self):
        try:
            import pymysql

            # Get connection details
            url = self.url_edit.text()
            username = self.user_edit.text()
            password = self.password_edit.text()
            port = self.port_edit.text()

            # Validate required fields
            if not url:
                raise ValueError("Database URL is required")
            if not username:
                raise ValueError("Username is required")

            # Use default port if not specified
            if not port:
                port = "3306"
                self.port_edit.setText(port)  # Update the port field with default value

            # Parse host from URL if needed
            host = url.split("/")[0] if "/" in url else url

            # Attempt to connect to the database
            connection = pymysql.connect(
                host=host,
                user=username,
                password=password,
                port=int(port),
                connect_timeout=5
            )

            # Test the connection by getting server version
            with connection.cursor() as cursor:
                cursor.execute("SELECT VERSION()")
                version = cursor.fetchone()

            connection.close()

            QMessageBox.information(None, "Connection Test", f"Connection successful!\nServer version: {version[0]}")
        except ImportError:
            QMessageBox.critical(None, "Module Error", "PyMySQL is not installed. Please install it using 'pip install pymysql'")
        except Exception as e:
            QMessageBox.critical(None, "Connection Failed", f"Could not connect: {str(e)}")