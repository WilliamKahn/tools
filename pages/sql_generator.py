from PySide6 import QtGui
from PySide6.QtWidgets import QVBoxLayout, QTableWidgetItem, QHBoxLayout, \
    QApplication, QMessageBox, QFrame
from PySide6.QtCore import Qt, QPoint
import re
from qfluentwidgets import TableWidget, PrimaryPushButton, TextEdit, RoundMenu, TeachingTip, InfoBarIcon, \
    TeachingTipTailPosition, Action, StyleSheetBase, FluentThemeColor, InfoBar, InfoBarPosition, FluentIcon


class SqlGenerator(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName('Page1')
        self.md_content = ""  # Initialize md_content
        self.initUI()
        self.column_map = {}
        self.attributes = ("字段", "类型", "备注")

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

        # Enable custom context menu
        self.tableWidget.horizontalHeader().setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.tableWidget.horizontalHeader().customContextMenuRequested[QPoint].connect(self.showContextMenu)

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

    def showContextMenu(self, pos):
        column = self.tableWidget.horizontalHeader().logicalIndexAt(pos)
        if column == -1:  # 如果没有点击到有效列，直接返回
            return
        contextMenu = RoundMenu(parent=self)

        for attribute in self.attributes:
            action = Action(text = attribute)
            action.triggered.connect(lambda checked, attr=attribute: self.setColumnFont(column, attr))
            contextMenu.addAction(action)

        resetAction = Action(text="Reset")
        resetAction.triggered.connect(lambda checked: self.setColumnFont(column, None))
        contextMenu.addAction(resetAction)
        contextMenu.exec_(self.tableWidget.horizontalHeader().mapToGlobal(pos))


    def setColumnFont(self, col, hint):
        header = self.tableWidget.horizontalHeaderItem(col)
        if header:
            if hint:
                self.resetColumnFont(hint)
                self.column_map[col] = (header.text(),hint)
                header.setText(hint)
            else:
                text = self.column_map[col][0]
                header.setText(text)
                if col in self.column_map:
                    del self.column_map[col]


    def resetColumnFont(self, hint):
        for col, col_hint in self.column_map.items():
            if col_hint[1] == hint:
                self.setColumnFont(col, None)
                break


    def showBottomTip(self):
        InfoBar.success(
            title='成功生成sql',
            content="成功拷贝到剪切板",
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
        col_name_index = -1
        col_type_index = -1
        col_comment_index = -1
        for i in range(col_count):
            header_item = self.tableWidget.horizontalHeaderItem(i)
            if header_item:
                if i in self.column_map:
                    hint = self.column_map[i][1]
                    if hint == "字段":
                        col_name_index = i
                    elif hint == "类型":
                        col_type_index = i
                    elif hint == "备注":
                        col_comment_index = i
        if col_name_index == -1 or col_type_index == -1:
            QMessageBox.warning(self, "Error", "No column selected as field.")
            return

        for i in range(row_count):
            col_name = self.tableWidget.item(i, col_name_index).text()
            col_type = self.tableWidget.item(i, col_type_index).text()
            col_comment = self.tableWidget.item(i, col_comment_index).text()
            columns.append(f"'{col_name}' {col_type} COMMENT '{col_comment}'")

        create_table_sql = f"CREATE TABLE table_name ({', '.join(columns)});"

        clipboard = QApplication.clipboard()
        clipboard.setText(create_table_sql)

        self.showBottomTip()