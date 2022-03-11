from keyring import get_password as keyring_get_password
from os.path import exists
from pwnedpasswords import check as pwned_check
from pysqlitecipher.sqlitewrapper import SqliteCipher
from pyperclip import copy as copy_to_cb
from secrets import choice as secrets_choice
from string import ascii_uppercase, ascii_lowercase, digits

from PySide6.QtCore import Qt, QSortFilterProxyModel
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QTableWidgetItem,
    QMessageBox,
    QLineEdit,
    QTableView,
    QHeaderView,
)
from PySide6.QtGui import QStandardItemModel, QStandardItem, QIcon

from ui_main_window import Ui_MainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setFixedWidth(710)
        self.setFixedHeight(530)

        # ----- Message Boxes -----
        self.dlg_no_password_selected = lambda: QMessageBox.warning(
            self,
            "Password Manager",
            "No password selected.",
            buttons=QMessageBox.Ok,
        )
        self.dlg_form_not_filled = lambda: QMessageBox.warning(
            self,
            "Password Manager",
            "All fields are required.",
            buttons=QMessageBox.Ok,
        )
        self.dlg_pwd_added = lambda: QMessageBox.information(
            self,
            "Password Manager",
            "Password has been added successfully.",
            buttons=QMessageBox.Ok,
        )
        self.dlg_delete_confirmation = lambda: QMessageBox.question(
            self,
            "Password Manager",
            "Are you sure you want to delete this password?",
            buttons=QMessageBox.No | QMessageBox.Yes,
        )
        # -------------------------

        # ----- Side-Menu -----
        self.ui.stackedWidget.setCurrentWidget(self.ui.widgetPasswords)
        self.ui.buttonTabPasswords.setStyleSheet(
            "background-color: #3d3d3d; border-left: 3px solid #8ab4f7"
        )
        self.ui.buttonTabPasswords.clicked.connect(self.show_passwords_tab)
        self.ui.buttonTabPasswords.clicked.connect(self.update_table)
        self.ui.buttonTabAddNew.clicked.connect(self.show_add_new_tab)
        self.ui.buttonTabGenerate.clicked.connect(self.show_generate_tab)
        self.ui.buttonTabHealth.clicked.connect(self.show_health_tab)
        self.generate_pwd()

        # ----- Password Dashboard ----------------
        self.ui.buttonDelete.clicked.connect(self.delete_password)
        self.ui.buttonCopyPassword.clicked.connect(self.copy_password)
        # ------------------------------------------

        # ----- Add New -----
        self.ui.buttonAddPassword.clicked.connect(self.update_db)
        self.ui.editTitle.returnPressed.connect(self.update_db)
        self.ui.editUrl.returnPressed.connect(self.update_db)
        self.ui.editUsername.returnPressed.connect(self.update_db)
        self.ui.editPassword.returnPressed.connect(self.update_db)
        self.ui.buttonClear.clicked.connect(self.clear_pwd_form)
        self.ui.buttonPasswordToggle.setCheckable(True)
        self.ui.buttonPasswordToggle.clicked.connect(self.password_toggle)

        # ----- Generate Password -----
        self.ui.horizontalSlider.valueChanged.connect(self.update_spin_box)
        self.ui.spinBox.valueChanged.connect(self.update_slider)
        self.ui.horizontalSlider.valueChanged.connect(self.generate_pwd)
        self.ui.spinBox.valueChanged.connect(self.generate_pwd)
        self.ui.checkBoxUpper.clicked.connect(self.generate_pwd)
        self.ui.checkBoxLower.clicked.connect(self.generate_pwd)
        self.ui.checkBoxDigits.clicked.connect(self.generate_pwd)
        self.ui.checkBoxSymbols.clicked.connect(self.generate_pwd)
        self.ui.buttonRegenerate.clicked.connect(self.generate_pwd)
        self.ui.buttonCopyRandomPassword.clicked.connect(
            self.copy_generated_pwd
        )

    # ----- Side-Menu -----
    def show_passwords_tab(self):
        """Highlights the 'Passwords' tab."""
        self.ui.buttonTabPasswords.setStyleSheet(
            "background-color: #3d3d3d; border-left: 4px solid #8ab4f7"
        )
        self.ui.buttonTabAddNew.setStyleSheet("")
        self.ui.buttonTabGenerate.setStyleSheet("")
        self.ui.buttonTabHealth.setStyleSheet("")
        self.ui.stackedWidget.setCurrentWidget(self.ui.widgetPasswords)

    def show_add_new_tab(self):
        """Highlights the 'Add New' tab."""
        self.ui.buttonTabPasswords.setStyleSheet("")
        self.ui.buttonTabAddNew.setStyleSheet(
            "background-color: #3d3d3d; border-left: 4px solid #8ab4f7"
        )
        self.ui.buttonTabGenerate.setStyleSheet("")
        self.ui.buttonTabHealth.setStyleSheet("")
        self.ui.stackedWidget.setCurrentWidget(self.ui.widgetAdd)

    def show_generate_tab(self):
        """Highlights the 'Generate Passwords' tab."""
        self.ui.buttonTabPasswords.setStyleSheet("")
        self.ui.buttonTabAddNew.setStyleSheet("")
        self.ui.buttonTabGenerate.setStyleSheet(
            "background-color: #3d3d3d; border-left: 4px solid #8ab4f7"
        )
        self.ui.buttonTabHealth.setStyleSheet("")
        self.ui.stackedWidget.setCurrentWidget(self.ui.widgetGenerate)

    def show_health_tab(self):
        """Highlights the 'Health Check' tab."""
        self.ui.buttonTabPasswords.setStyleSheet("")
        self.ui.buttonTabAddNew.setStyleSheet("")
        self.ui.buttonTabGenerate.setStyleSheet("")
        self.ui.buttonTabHealth.setStyleSheet(
            "background-color: #3d3d3d; border-left: 4px solid #8ab4f7"
        )
        self.ui.stackedWidget.setCurrentWidget(self.ui.widgetHealth)

    def get_db(self):
        """Returns the password database."""
        return SqliteCipher(
            dataBasePath="Password_Manager.db",
            checkSameThread=True,
            password=keyring_get_password("Password Manager", "user"),
        )

    def db_create_passwords_table(self):
        db = self.get_db()
        db.createTable(
            "Password",
            [
                ["title", "TEXT"],
                ["url", "TEXT"],
                ["username", "TEXT"],
                ["password", "TEXT"],
                ["compromised", "INT"],
            ],
            makeSecure=True,
            commit=True,
        )

    # ----- Password Dashboard -----
    def update_table(self):
        """Inserts the data from the database into the passwords table."""
        data = self.get_table_data()
        model = QStandardItemModel(len(data), 3)
        model.setHorizontalHeaderLabels(
            ["Title", "URL", "Username", "Password"]
        )

        for row_num in range(len(data)):
            for col_num, col_data in enumerate(data[row_num]):
                if col_num == 3:
                    col_data = "".join("*" for i in range(len(col_data)))
                model.setItem(row_num, col_num, QStandardItem(col_data))

        filter_proxy_model = QSortFilterProxyModel()
        filter_proxy_model.setSourceModel(model)
        filter_proxy_model.setFilterCaseSensitivity(Qt.CaseInsensitive)
        filter_proxy_model.setFilterKeyColumn(0)

        self.ui.tablePasswords.setModel(filter_proxy_model)

        self.ui.editSearch.textChanged.connect(
            filter_proxy_model.setFilterRegularExpression
        )

    def delete_password(self):
        """Removes the selected row from the database."""
        db = self.get_db()
        try:
            selected_row = self.ui.tablePasswords.selectedIndexes()[3].row()

            if self.dlg_delete_confirmation() == QMessageBox.Yes:
                db.deleteDataInTable("Password", selected_row)
                self.update_table()
        except IndexError:
            self.dlg_no_password_selected()

    def edit_password(self):
        """Removes the entity of the selected row."""
        db = self.get_db()
        try:
            selected_row = self.ui.tablePasswords.selectedIndexes()[3].row()
            db.deleteDataInTable("Password", selected_row)
            self.update_table()
        except IndexError:
            self.dlg_no_password_selected()

    def copy_password(self):
        db = self.get_db()
        try:
            selected_row = self.ui.tablePasswords.selectedIndexes()[3].row()
            selected_col = self.ui.tablePasswords.selectedIndexes()[3].column()
            copy_to_cb(
                db.getDataFromTable(
                    "Password", raiseConversionError=True, omitID=True
                )[1:][0][selected_row][selected_col]
            )
        except IndexError:
            self.dlg_no_password_selected()

    # ----- Add New -----
    def update_db(self):
        """Inserts the data from the 'Add New' form into the database."""
        db = self.get_db()
        data = [
            self.ui.editTitle.text(),
            self.ui.editUrl.text(),
            self.ui.editUsername.text(),
            self.ui.editPassword.text(),
            self.is_password_compromised(self.ui.editPassword.text()),
        ]
        for row_num, row_data in enumerate(data):
            if row_num == len(data) - 1:
                db.insertIntoTable(
                    tableName="Password",
                    insertList=data,
                    commit=True,
                )
                self.dlg_pwd_added()
                self.clear_pwd_form()
            if row_num != 3 and str(row_data).replace(" ", "") == "":
                self.dlg_form_not_filled()
                break

    def password_toggle(self, checked):
        if checked:
            self.ui.editPassword.setEchoMode(QLineEdit.EchoMode.Normal)
            self.ui.buttonPasswordToggle.setIcon(QIcon("icons/eye.svg"))
        else:
            self.ui.editPassword.setEchoMode(QLineEdit.EchoMode.Password)
            self.ui.buttonPasswordToggle.setIcon(
                QIcon("icons/eye-crossed.svg")
            )

    def is_password_compromised(self, password):
        return (
            1 if pwned_check(password, plain_text=True, anonymous=True) else 0
        )

    def clear_pwd_form(self):
        self.ui.editTitle.clear()
        self.ui.editUsername.clear()
        self.ui.editUrl.clear()
        self.ui.editPassword.clear()

    # ----- Generate Password -----
    def update_spin_box(self):
        self.ui.spinBox.setValue(self.ui.horizontalSlider.value())

    def update_slider(self):
        self.ui.horizontalSlider.setValue(self.ui.spinBox.value())

    def generate_pwd(self):
        len = self.ui.spinBox.value()

        characters = ""
        types_checked = 1
        if self.ui.checkBoxUpper.isChecked():
            characters += ascii_uppercase
        if self.ui.checkBoxLower.isChecked():
            characters += ascii_lowercase
        if self.ui.checkBoxDigits.isChecked():
            characters += digits
        if self.ui.checkBoxSymbols.isChecked():
            characters += "@%$!&?#"

        random_pwd = "".join(secrets_choice(characters) for i in range(len))

        self.ui.labelGeneratedPwd.setText(random_pwd)

    def copy_generated_pwd(self):
        copy_to_cb(self.ui.labelGeneratedPwd.text())

    def get_table_data(self):
        db = self.get_db()
        if not db.checkTableExist("Password"):
            self.db_create_passwords_table()
        return db.getDataFromTable(
            "Password", raiseConversionError=True, omitID=True
        )[1:][0]
