from PySide6.QtWidgets import (QVBoxLayout, QTableWidgetItem, QHBoxLayout,
                               QApplication, QFrame, QTableWidget, QPushButton,
                               QTextEdit, QMessageBox, QLabel)
from PySide6.QtCore import Qt, QTimer
import re


class SqlGenerator(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName('SqlGenerator')
        self.initUI()

    def initUI(self):
        layout = QHBoxLayout()

        # Left side: QTextEdit
        self.textEdit = QTextEdit()
        layout.addWidget(self.textEdit)

        # Right side: QTableWidget and QPushButton
        right_layout = QVBoxLayout()
        self.tableWidget = QTableWidget()
        right_layout.addWidget(self.tableWidget)

        self.sqlButton = QPushButton("Generate SQL", self)
        self.sqlButton.clicked.connect(self.generateSQL)
        right_layout.addWidget(self.sqlButton)

        layout.addLayout(right_layout)
        self.setLayout(layout)

        self.textEdit.textChanged.connect(self.updateTable)

    def updateTable(self):
        # Since PySide6 QTextEdit doesn't have toMarkdown method
        # we'll use toPlainText instead
        md_content = self.textEdit.toPlainText()
        rows = []
        # todo 格式校验
        # 格式转换
        if '|' in md_content:
            # Markdown table format
            lines = md_content.split('\n')
            rows = [line.split('|') for line in lines if '|' in line]
            for i in range(len(rows)):
                rows[i] = rows[i][1:-1]
            rows = [rows[0]] + rows[2:]  # Skip the separator line
        else:
            # Plain text table format
            lines = md_content.split('\n')
            headers = re.split(r'\s+|\t', lines[0])
            split = len(headers)
            rows.append(headers)
            for line in lines[1:]:
                rows.append(re.split(r'\s+|\t', line, maxsplit=split - 1))

        if rows:
            headers = [header.strip() for header in rows[0]]
            self.tableWidget.setColumnCount(len(headers))
            self.tableWidget.setHorizontalHeaderLabels(headers)

            self.tableWidget.setRowCount(len(rows) - 1)
            for i, row in enumerate(rows[1:]):
                for j, cell in enumerate(row):
                    if j < len(headers):  # Check to prevent index error
                        self.tableWidget.setItem(i, j, QTableWidgetItem(cell.strip()))
        # 列校验 采用特征叠加判断具体列

    def showBottomTip(self):
        # Replace InfoBar with a temporary notification
        temp_label = QLabel('成功生成sql，已经复制到剪切板', self)
        temp_label.setStyleSheet("background-color: #2196F3; color: white; padding: 8px; border-radius: 4px;")
        temp_label.setAlignment(Qt.AlignCenter)

        # Position at top
        temp_label.setGeometry(self.width() // 2 - 150, 10, 300, 40)
        temp_label.show()

        # Hide after 2 seconds
        QTimer.singleShot(2000, temp_label.deleteLater)

    def generateSQL(self):
        row_count = self.tableWidget.rowCount()
        col_count = self.tableWidget.columnCount()
        columns = []
        if col_count < 2:
            QMessageBox.critical(self, "Error", "less than 2 columns")
            return

        flag = False
        for i in range(row_count):
            item0 = self.tableWidget.item(i, 0)
            item1 = self.tableWidget.item(i, 1)
            if not item0 or not item1:
                continue

            col_name = item0.text()
            if col_name == "id":
                flag = True
            col_type = item1.text()

            if col_count > 2:
                item2 = self.tableWidget.item(i, 2)
                col_comment = item2.text() if item2 else ""
                columns.append(f"\n`{col_name}` {col_type} COMMENT '{col_comment}'")
            else:
                columns.append(f"\n`{col_name}` {col_type}")

        if flag:
            columns.append(f"\nPRIMARY KEY (`id`)\n")

        create_table_sql = f"CREATE TABLE IF NOT EXISTS `table_name` ({','.join(columns)})"
        create_table_sql += f" ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='test';"
        clipboard = QApplication.clipboard()
        clipboard.setText(create_table_sql)

        self.showBottomTip()

    def serialize(self):
        """序列化保存配置数据"""
        data = {
            "markdown_content": self.textEdit.toPlainText()  # Using toPlainText instead of toMarkdown
        }
        return data

    def deserialize(self, data):
        """反序列化加载配置数据"""
        if "markdown_content" in data:
            self.textEdit.setPlainText(data["markdown_content"])  # Using setPlainText instead of setMarkdown
            # updateTable will be called through the signal connection