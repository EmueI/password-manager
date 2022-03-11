from keyring import get_password as keyring_get_password
from os.path import exists
from pwnedpasswords import check as pwned_check
from pysqlitecipher.sqlitewrapper import SqliteCipher
from pyperclip import copy as copy_to_cb
from secrets import choice as secrets_choice
from string import ascii_uppercase, ascii_lowercase, digits

from PySide6.QtCore import QSortFilterProxyModel
from PySide6.QtWidgets import QMainWindow, QTableWidgetItem, QMessageBox
from PySide6.QtGui import QStandardItemModel, QStandardItem

from ui_main_window import Ui_MainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setFixedWidth(710)
        self.setFixedHeight(530)

        # ----- Side-Menu -----
        self.ui.stackedWidget.setCurrentWidget(self.ui.widgetPasswords)
        self.ui.buttonTabPasswords.setStyleSheet(
            "background-color: #3d3d3d; border-left: 3px solid #8ab4f7"
        )
        self.ui.buttonTabPasswords.clicked.connect(self.show_passwords_tab)
        self.ui.buttonTabPasswords.clicked.connect(self.update_table)
        self.ui.buttonTabAddNew.clicked.connect(self.show_add_new_tab)
        self.ui.buttonTabGenerate.clicked.connect(self.show_generate_tab)
        self.ui.buttonTabSecurity.clicked.connect(self.show_security_tab)

        # ----- Password Dashboard ----------------
        self.dlg_no_passwords = QMessageBox(self)
        self.dlg_no_passwords.setWindowTitle("Password Manager")
        self.dlg_no_passwords.setText("No passwords found.")
        self.dlg_no_passwords.setStandardButtons(QMessageBox.Ok)
        self.dlg_no_passwords.setIcon(QMessageBox.Warning)
        self.ui.buttonCopyPwd.clicked.connect(self.copy_pwd)

        # ----- Search Feature -----
        self.ui.editSearch.textChanged.connect(self.table_search)
        # ------------------------------------------

        # ----- Add New -----
        self.dlg_form_not_filled = QMessageBox(self)
        self.dlg_form_not_filled.setWindowTitle("Password Manager")
        self.dlg_form_not_filled.setText("All fields are required.")
        self.dlg_form_not_filled.setStandardButtons(QMessageBox.Ok)
        self.dlg_form_not_filled.setIcon(QMessageBox.Warning)

        self.dlg_pwd_added = QMessageBox(self)
        self.dlg_pwd_added.setWindowTitle("Password Manager")
        self.dlg_pwd_added.setText("Password has been added successfully.")
        self.dlg_pwd_added.setStandardButtons(QMessageBox.Ok)
        self.dlg_pwd_added.setIcon(QMessageBox.Information)

        self.ui.buttonAddPassword.clicked.connect(self.update_db)
        self.ui.editTitle.returnPressed.connect(self.update_db)
        self.ui.editUrl.returnPressed.connect(self.update_db)
        self.ui.editUsername.returnPressed.connect(self.update_db)
        self.ui.editPassword.returnPressed.connect(self.update_db)
        self.ui.buttonClear.clicked.connect(self.clear_pwd_form)

        # ----- Generate Password -----
        self.dlg_no_type_selected = QMessageBox(self)
        self.dlg_no_type_selected.setWindowTitle("Password Manager")
        self.dlg_no_type_selected.setText(
            "Select at least one character type."
        )
        self.dlg_no_type_selected.setStandardButtons(QMessageBox.Ok)
        self.dlg_no_type_selected.setIcon(QMessageBox.Warning)

        self.ui.horizontalSlider.valueChanged.connect(self.update_spin_box)
        self.ui.spinBox.valueChanged.connect(self.update_slider)
        self.ui.buttonGeneratePwd.clicked.connect(self.generate_pwd)
        self.ui.buttonCopyRandomPwd.clicked.connect(self.copy_generated_pwd)

    # ----- Side-Menu -----
    def show_passwords_tab(self):
        """Highlights the 'Passwords' tab."""
        self.ui.buttonTabPasswords.setStyleSheet(
            "background-color: #3d3d3d; border-left: 3px solid #8ab4f7"
        )
        self.ui.buttonTabAddNew.setStyleSheet("")
        self.ui.buttonTabGenerate.setStyleSheet("")
        self.ui.buttonTabSecurity.setStyleSheet("")
        self.ui.stackedWidget.setCurrentWidget(self.ui.widgetPasswords)

    def show_add_new_tab(self):
        """Highlights the 'Add New' tab."""
        self.ui.buttonTabPasswords.setStyleSheet("")
        self.ui.buttonTabAddNew.setStyleSheet(
            "background-color: #3d3d3d; border-left: 3px solid #8ab4f7"
        )
        self.ui.buttonTabGenerate.setStyleSheet("")
        self.ui.buttonTabSecurity.setStyleSheet("")
        self.ui.stackedWidget.setCurrentWidget(self.ui.widgetAdd)

    def show_generate_tab(self):
        """Highlights the 'Generate Passwords' tab."""
        self.ui.buttonTabPasswords.setStyleSheet("")
        self.ui.buttonTabAddNew.setStyleSheet("")
        self.ui.buttonTabGenerate.setStyleSheet(
            "background-color: #3d3d3d; border-left: 3px solid #8ab4f7"
        )
        self.ui.buttonTabSecurity.setStyleSheet("")
        self.ui.stackedWidget.setCurrentWidget(self.ui.widgetGenerate)

    def show_security_tab(self):
        """Highlights the 'Security Check' tab."""
        self.ui.buttonTabPasswords.setStyleSheet("")
        self.ui.buttonTabAddNew.setStyleSheet("")
        self.ui.buttonTabGenerate.setStyleSheet("")
        self.ui.buttonTabSecurity.setStyleSheet(
            "background-color: #3d3d3d; border-left: 3px solid #8ab4f7"
        )
        self.ui.stackedWidget.setCurrentWidget(self.ui.widgetSecurity)

    def get_db(self):
        """Returns the database."""
        return SqliteCipher(
            dataBasePath="Password_Manager.db",
            checkSameThread=True,
            password=keyring_get_password("Password Manager", "user"),
        )

    def create_passwords_table(self):
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
        db = self.get_db()
        if not db.checkTableExist("Password"):
            self.create_passwords_table()
        data = db.getDataFromTable(
            "Password", raiseConversionError=True, omitID=True
        )[1:][0]
        self.ui.tablePasswords.setRowCount(0)
        for row_number, row_data in enumerate(data):
            self.ui.tablePasswords.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                if column_number == 3:
                    data = "".join("*" for i in range(len(data)))
                self.ui.tablePasswords.setItem(
                    row_number, column_number, QTableWidgetItem(str(data))
                )
        self.ui.tablePasswords.setColumnWidth(0, 70)
        self.ui.tablePasswords.setColumnWidth(1, 150)
        self.ui.tablePasswords.setColumnWidth(2, 100)

    def copy_pwd(self):
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
            self.dlg_no_passwords.exec()

    def table_search(self):
        data = self.get_table_data()
        titles = [data[row][0] for row in range(len(data))]

    # ----- Add New -----
    def update_db(self):
        """Inserts the data from the 'Add New' form into the database."""
        db = self.get_db()
        if not db.checkTableExist("Password"):
            self.create_passwords_table()
        data = [
            self.ui.editTitle.text(),
            self.ui.editUrl.text(),
            self.ui.editUsername.text(),
            self.ui.editPassword.text(),
            self.is_password_compromised(self.ui.editPassword.text()),
        ]
        for row_number, row_data in enumerate(data):
            if row_data == "":
                self.dlg_form_not_filled.exec()
                break
            if row_number == len(data) - 1:
                db.insertIntoTable(
                    tableName="Password",
                    insertList=data,
                    commit=True,
                )
                self.dlg_pwd_added.exec()
                self.clear_pwd_form()

    def delete_password(self, id):
        pass

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
        self.ui.labelCopiedToClip.clear()
        len = self.ui.spinBox.value()

        characters = ""
        if self.ui.checkBoxUpper.isChecked():
            characters += ascii_uppercase
        if self.ui.checkBoxLower.isChecked():
            characters += ascii_lowercase
        if self.ui.checkBoxDigits.isChecked():
            characters += digits
        if self.ui.checkBoxSymbols.isChecked():
            characters += "!$%@#"

        try:
            random_pwd = "".join(
                secrets_choice(characters) for i in range(len)
            )
            self.ui.labelGeneratedPwd.setText(random_pwd)
        except:
            self.dlg_no_type_selected.exec()

    def copy_generated_pwd(self):
        copy_to_cb(self.ui.labelGeneratedPwd.text())
        self.ui.labelCopiedToClip.setText("Copied to clipboard.")

    def get_table_data(self):
        db = self.get_db()
        return db.getDataFromTable(
            "Password", raiseConversionError=True, omitID=True
        )[1:][0]
