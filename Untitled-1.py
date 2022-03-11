import sys
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QLineEdit,
    QTableView,
    QHeaderView,
    QVBoxLayout,
    QAbstractItemView,
    QHeaderView
)
from PySide6.QtCore import Qt, QSortFilterProxyModel
from PySide6.QtGui import QStandardItemModel, QStandardItem


class AppDemo(QWidget):
    def __init__(self):
        super().__init__()
        mainLayout = QVBoxLayout()

        data = [
            [
                "Apple",
                "Facebook",
                "Google",
                "Amazon",
                "Walmart",
                "Dropbox",
                "Starbucks",
                "eBay",
                "Canon",
            ],
            [
                "https://apple.com",
                "https://facebook.com",
                "https://google.com",
                "https://amazon.com",
                "https://walmart.com",
                "https://dropbox.com",
                "https://starbucks.com",
                "https://ebay.com",
                "https://canon.com",
            ],
            [
                "jeff1",
                "jeffery@gmail.com",
                "jeffery@gmail.com",
                "jeff1",
                "jeff1",
                "https://fveasefvafv.com",
                "jeffery@gmail.com",
                "jeff1",
                "jeffery@gmail.com",
            ],
        ]

        model = QStandardItemModel(len(data[0]), len(data))
        model.setHorizontalHeaderLabels(
            ["Title", "URL", "Username", "Password"]
        )

        # Adding the data into the model.
        for col in range(len(data)):
            for row_num, row_data in enumerate(data[col]):
                model.setItem(row_num, col, QStandardItem(row_data))

        filter_proxy_model = QSortFilterProxyModel()
        filter_proxy_model.setSourceModel(model)
        filter_proxy_model.setFilterCaseSensitivity(Qt.CaseInsensitive)
        filter_proxy_model.setFilterKeyColumn(0)

        search_field = QLineEdit()
        search_field.textChanged.connect(
            filter_proxy_model.setFilterRegularExpression
        )
        mainLayout.addWidget(search_field)

        table = QTableView()
        table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table.setModel(filter_proxy_model)
        table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        table.verticalHeader().hide()
        mainLayout.addWidget(table)

        self.setLayout(mainLayout)


app = QApplication(sys.argv)
demo = AppDemo()
demo.show()
sys.exit(app.exec())
