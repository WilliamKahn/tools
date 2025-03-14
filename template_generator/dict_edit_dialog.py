from PySide6.QtWidgets import QDialog, QHBoxLayout, QVBoxLayout, QPushButton, QTableWidgetItem, QSplitter, QWidget
from qfluentwidgets import TableWidget, BodyLabel

class DictionaryEditorDialog(QDialog):

    def __init__(self, extra_mappings):
        super().__init__()
        self.setWindowTitle("Edit Dictionary")
        self.resize(600, 400)
        self.extra_mappings = extra_mappings
        self.initUI()
        self.load_dictionary_data(extra_mappings)

    def initUI(self):
        main_layout = QHBoxLayout(self)

        # Splitter to divide the main layout
        splitter = QSplitter()
        main_layout.addWidget(splitter)

        # Left section for map_section
        map_section = QVBoxLayout()
        map_widget = QWidget()
        map_widget.setLayout(map_section)
        splitter.addWidget(map_widget)

        # Table for dictionary entries
        self.table = TableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Key", "Value"])
        map_section.addWidget(self.table)

        # Buttons for adding and deleting rows
        button_layout = QHBoxLayout()
        self.add_row_button = QPushButton("Add Row")
        self.add_row_button.clicked.connect(self.add_row)
        button_layout.addWidget(self.add_row_button)

        self.delete_row_button = QPushButton("Delete Row")
        self.delete_row_button.clicked.connect(self.delete_row)
        button_layout.addWidget(self.delete_row_button)

        map_section.addLayout(button_layout)

        # Right section for description label
        right_section = QVBoxLayout()
        right_widget = QWidget()
        right_widget.setLayout(right_section)
        splitter.addWidget(right_widget)

        self.description_label = BodyLabel("Description information goes here.")
        right_section.addWidget(self.description_label)

        # Set the splitter ratio
        splitter.setStretchFactor(0, 2)
        splitter.setStretchFactor(1, 1)

        self.setLayout(main_layout)

    def add_row(self):
        row_position = self.table.rowCount()
        self.table.insertRow(row_position)
        self.table.setItem(row_position, 0, QTableWidgetItem("Key"))
        self.table.setItem(row_position, 1, QTableWidgetItem("Value"))

    def delete_row(self):
        current_row = self.table.currentRow()
        if current_row >= 0:
            self.table.removeRow(current_row)

    def load_dictionary_data(self, extra_mappings):
        # Clear existing rows
        self.table.setRowCount(0)

        # Populate table with dictionary data
        for key, value in extra_mappings.items():
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            self.table.setItem(row_position, 0, QTableWidgetItem(str(key)))
            self.table.setItem(row_position, 1, QTableWidgetItem(str(value)))

    def closeEvent(self, arg__1, /):
        self.extra_mappings.clear()
        for row in range(self.table.rowCount()):
            key_item = self.table.item(row, 0)
            value_item = self.table.item(row, 1)
            key = key_item.text()
            value = value_item.text()
            self.extra_mappings[key] = value