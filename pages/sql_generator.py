from PySide6.QtWidgets import QVBoxLayout, QTableWidgetItem, QHBoxLayout, \
    QApplication, QFrame
from PySide6.QtCore import Qt
import re
from qfluentwidgets import TableWidget, PrimaryPushButton, TextEdit, InfoBar, InfoBarPosition, MessageBox


class SqlGenerator(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName('Page1')
        self.initUI()

    def initUI(self):
        layout = QHBoxLayout()

        # Left side: QTextEdit
        self.textEdit = TextEdit()
        layout.addWidget(self.textEdit)

        # Right side: QTableWidget and QPushButton
        right_layout = QVBoxLayout()
        self.tableWidget = TableWidget()
        right_layout.addWidget(self.tableWidget)

        self.sqlButton = PrimaryPushButton("Generate SQL",self)
        self.sqlButton.clicked.connect(self.generateSQL)
        right_layout.addWidget(self.sqlButton)

        layout.addLayout(right_layout)
        self.setLayout(layout)

        self.textEdit.textChanged.connect(self.updateTable)

    def updateTable(self):
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
                    self.tableWidget.setItem(i, j, QTableWidgetItem(cell.strip()))
        # 列校验 采用特征叠加判断具体列


    def showBottomTip(self):
        InfoBar.success(
            title='成功生成sql',
            content="已经复制到剪切板",
            orient=Qt.Orientation.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP,
            # position='Custom',   # NOTE: use custom info bar manager
            duration=2000,
            parent=self
        )

    def generateSQL(self):
        row_count = self.tableWidget.rowCount()
        col_count = self.tableWidget.columnCount()
        columns = []
        if col_count < 2:
            MessageBox( "Error", "less than 2 columns",self).exec()
            return

        for i in range(row_count):
            col_name = self.tableWidget.item(i, 0).text()
            col_type = self.tableWidget.item(i, 1).text()
            if col_count > 2:
                col_comment = self.tableWidget.item(i, 2).text()
                columns.append(f"'{col_name}' {col_type} COMMENT '{col_comment}'")
            else:
                columns.append(f"'{col_name}' {col_type}")

        create_table_sql = f"CREATE TABLE table_name ({', '.join(columns)});"

        clipboard = QApplication.clipboard()
        clipboard.setText(create_table_sql)

        self.showBottomTip()