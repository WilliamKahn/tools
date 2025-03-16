import os

from PySide6.QtWidgets import QVBoxLayout, QFrame, QFileDialog, QListWidgetItem, QHBoxLayout, QLabel, QComboBox, \
    QPushButton, QLineEdit, QListWidget, QScrollArea, QWidget
from template_generator.db_config_dialog import DatabaseConfigDialog
from template_generator.db_config_model import DBConfigModel
from template_generator.dict_edit_dialog import DictionaryEditorDialog
from template_generator.generator import generate
from template_generator.list_item import ListItemWidget


class TemplateGenerator(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName('TemplateGenerator')
        self.db_config = DBConfigModel()
        self.extra_mappings = {}
        self.list = []
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        db_section = QHBoxLayout()
        # Label
        db_section.addWidget(QLabel(text = "Database:"))

        # Dropdown for selecting database configuration
        self.db_combo = QComboBox()
        self.db_combo.setMinimumWidth(200)
        self.db_config.dataChanged.connect(self.update_combo)
        db_section.addWidget(self.db_combo)

        # Edit button for database configurations
        self.db_edit_button = QPushButton("Edit")
        self.db_edit_button.clicked.connect(self.edit_db_config)
        db_section.addWidget(self.db_edit_button)

        self.db_name = QLineEdit()
        self.db_name.setPlaceholderText("Database Name")
        db_section.addWidget(self.db_name)

        self.table_name = QLineEdit()
        self.table_name.setPlaceholderText("Table Name")
        db_section.addWidget(self.table_name)

        self.dict_edit_button = QPushButton("Extra")
        self.dict_edit_button.clicked.connect(self.edit_dictionary)
        db_section.addWidget(self.dict_edit_button)

        db_section.addStretch(1)
        layout.addLayout(db_section)

        # Configuration part: Button to select project path
        self.config_button = QPushButton("Select Project Path")
        self.config_button.clicked.connect(self.select_project_path)
        layout.addWidget(self.config_button)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_area.setWidget(self.scroll_content)
        layout.addWidget(self.scroll_area)
        # List widget to hold list items
        # self.list_widget = QListWidget()
        # layout.addWidget(self.list_widget)

        # Add a sample list item
        self.load_files("./template")

        self.generate_button = QPushButton("Generate files")
        self.generate_button.clicked.connect(self.on_generate_button_clicked)
        layout.addWidget(self.generate_button)

        self.setLayout(layout)

    def select_project_path(self):
        path = QFileDialog.getExistingDirectory(self, "Select Project Path")
        if path:
            self.config_button.setText(path)
            self.config_button.setToolTip(path)

    def load_files(self, directory):
        # self.list_widget.clear()
        for file_name in os.listdir(directory):
            file_path = os.path.join(directory, file_name)
            if os.path.isfile(file_path):
                # list_item = QListWidgetItem(self.list_widget)
                list_item_widget = ListItemWidget(file_path)
                self.list.append(list_item_widget)
                # self.list_widget.setItemWidget(list_item, list_item_widget)
                self.scroll_layout.addWidget(list_item_widget)

    def edit_db_config(self):
        dialog = DatabaseConfigDialog(self.db_config)
        dialog.exec_()

    def edit_dictionary(self):
        dialog = DictionaryEditorDialog(self.extra_mappings)
        dialog.exec_()

    def on_generate_button_clicked(self):
        database = self.db_config.get_data()[self.db_combo.currentText()]
        db = self.db_name.text()
        table = self.table_name.text()
        project_path = self.config_button.toolTip()
        extra = self.extra_mappings
        files = self.get_list_items_data()
        generate(database, db,table, project_path, extra, files)

    def get_list_items_data(self):
        items_data = {}
        for item in self.list:
            is_checked = item.checkbox.isChecked()
            file_path = item.file_path
            module_path = item.module_button.toolTip()
            package_path = item.package_button.toolTip()
            alias = item.alias_edit.text()
            items_data[file_path] = [
                is_checked,
                module_path,
                package_path,
                alias
            ]
        return items_data

    def serialize(self):
        return {
            "db_configs": self.db_config.get_data(),
            "extra_mappings": self.extra_mappings,
            "project_path": self.config_button.toolTip(),
            "list_items": self.get_list_items_data(),
            "db_name": self.db_name.text(),
            "table_name": self.table_name.text()
        }

    def deserialize(self, param):
        if "db_configs" in param:
            self.db_config.set_data(param["db_configs"])
        if "extra_mappings" in param:
            self.extra_mappings= param["extra_mappings"]
        if "project_path" in param:
            if os.path.isdir(param["project_path"]):
                self.config_button.setText(param["project_path"])
                self.config_button.setToolTip(param["project_path"])
        if "db_name" in param:
            self.db_name.setText(param["db_name"])
        if "table_name" in param:
            self.table_name.setText(param["table_name"])
        if "list_items" in param:
            for file_path, data in param["list_items"].items():
                for item in self.list:
                    if item.file_path == file_path:
                        item.checkbox.setChecked(data[0])
                        if data[1]:
                            item.module_button.setText(os.path.basename(data[1]))
                            item.module_button.setToolTip(data[1])
                        if data[2]:
                            item.package_button.setText(os.path.basename(data[2]))
                            item.package_button.setToolTip(data[2])
                        item.alias_edit.setText(data[3])
                        break

    def update_combo(self, items):
        self.db_combo.clear()
        self.db_combo.addItems(items)