from PyQt5.QtGui import QIcon, QPixmap, QPainter, QColor, QBrush
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QHBoxLayout, \
    QApplication, QMenu, QAction, QMessageBox, QPlainTextEdit
from PyQt5.QtCore import Qt
import re


class Page1(QWidget):
    def __init__(self):
        super().__init__()
        self.md_content = ""  # Initialize md_content
        self.initUI()
        self.column_colors = {}
        self.attributes = (
            {'name': "字段",'color': Qt.red},
            {'name': "类型",'color': Qt.green},
            {'name': "备注", 'color': Qt.gray})

    def initUI(self):
        layout = QHBoxLayout()

        # Left side: QTextEdit
        self.textEdit = QPlainTextEdit()
        layout.addWidget(self.textEdit)

        # Right side: QTableWidget and QPushButton
        right_layout = QVBoxLayout()
        self.tableWidget = QTableWidget()
        right_layout.addWidget(self.tableWidget)

        self.sqlButton = QPushButton("Generate SQL")
        self.sqlButton.clicked.connect(self.generateSQL)
        right_layout.addWidget(self.sqlButton)

        layout.addLayout(right_layout)
        self.setLayout(layout)

        self.textEdit.textChanged.connect(self.updateTable)

        # Enable custom context menu
        self.tableWidget.horizontalHeader().setContextMenuPolicy(Qt.CustomContextMenu)
        self.tableWidget.horizontalHeader().customContextMenuRequested.connect(self.showContextMenu)

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
        contextMenu = QMenu(self)

        for attribute in self.attributes:
            Icon = self.createColorIcon(attribute['color'])
            action = QAction(Icon, attribute['name'], self)
            contextMenu.addAction(action)

        resetAction = QAction("Reset", self)
        contextMenu.addAction(resetAction)

        action = contextMenu.exec_(self.tableWidget.mapToGlobal(pos))
        if action:
            col = self.tableWidget.horizontalHeader().logicalIndexAt(pos)
            for attribute in self.attributes:
                if action.text() == attribute['name']:
                    self.resetColumnColor(attribute['color'])
                    self.setColumnColor(col, attribute['color'])
                    break
            if action == resetAction:
                self.setColumnColor(col, None)

    def createColorIcon(self, color):
        pixmap = QPixmap(16, 16)
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        painter.setBrush(QColor(color))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(6, 6, 4, 4)
        painter.end()
        return QIcon(pixmap)

    def resetColumnColor(self, color):
        for col, col_color in self.column_colors.items():
            if col_color == color:
                self.setColumnColor(col, None)
                break

    def setColumnColor(self, col, color):
        header = self.tableWidget.horizontalHeaderItem(col)
        if header:
            if color:
                header.setForeground(QBrush(color))
                self.column_colors[col] = color
            else:
                header.setForeground(QBrush())
                if col in self.column_colors:
                    del self.column_colors[col]

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
                if i in self.column_colors:
                    color = self.column_colors[i]
                    if color == Qt.red:
                        col_name_index = i
                    elif color == Qt.green:
                        col_type_index = i
                    elif color == Qt.gray:
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
