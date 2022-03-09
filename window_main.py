from keyring import get_password as keyring_get_password
from os.path import exists
from pwnedpasswords import check as pwned_check
from pysqlitecipher.sqlitewrapper import SqliteCipher
from pyperclip import copy
from secrets import choice as secrets_choice
from string import ascii_uppercase, ascii_lowercase, digits

from PySide6.QtWidgets import QMainWindow, QTableWidgetItem, QMessageBox

from ui_main_window import Ui_MainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setFixedWidth(660)
        self.setFixedHeight(500)

        # ----- Side-Menu -----
        self.ui.stackedWidget.setCurrentWidget(self.ui.widgetPasswords)
        self.ui.buttonPasswords.setStyleSheet("background-color: #3d3d3d")
        self.ui.buttonPasswords.clicked.connect(self.show_passwords)
        self.ui.buttonAddNew.clicked.connect(self.show_add_new)
        self.ui.buttonGenerate.clicked.connect(self.show_generate)
        self.ui.buttonSecurity.clicked.connect(self.show_security)

        # ----- Password Dashboard -----

        # ----- Add New -----
        self.ui.buttonAddPassword.clicked.connect(self.update_table)
        self.ui.buttonAddPassword.clicked.connect(self.update_db)
        self.ui.buttonClear.clicked.connect(self.clear_pwd_form)

        # ----- Generate Password -----
        self.dlg_none_selected = QMessageBox(self)
        self.dlg_none_selected.setWindowTitle("Password Vault")
        self.dlg_none_selected.setText("Choose at least one option.")
        self.dlg_none_selected.setStandardButtons(QMessageBox.Ok)
        self.dlg_none_selected.setIcon(QMessageBox.Warning)

        self.ui.horizontalSlider.valueChanged.connect(self.update_spin_box)
        self.ui.spinBox.valueChanged.connect(self.update_slider)
        self.ui.buttonGeneratePwd.clicked.connect(self.generate_pwd)
        self.ui.buttonCopyPwd.clicked.connect(self.copy_generated_pwd)

    # ----- Side-Menu -----
    def show_passwords(self):
        """Highlights the 'Passwords' tab."""
        self.ui.buttonPasswords.setStyleSheet("background-color: #3d3d3d")
        self.ui.buttonAddNew.setStyleSheet("")
        self.ui.buttonGenerate.setStyleSheet("")
        self.ui.buttonSecurity.setStyleSheet("")
        self.ui.stackedWidget.setCurrentWidget(self.ui.widgetPasswords)

    def show_add_new(self):
        """Highlights the 'Add New' tab."""
        self.ui.buttonPasswords.setStyleSheet("")
        self.ui.buttonAddNew.setStyleSheet("background-color: #3d3d3d")
        self.ui.buttonGenerate.setStyleSheet("")
        self.ui.buttonSecurity.setStyleSheet("")
        self.ui.stackedWidget.setCurrentWidget(self.ui.widgetAdd)

    def show_generate(self):
        """Highlights the 'Generate Passwords' tab."""
        self.ui.buttonPasswords.setStyleSheet("")
        self.ui.buttonAddNew.setStyleSheet("")
        self.ui.buttonGenerate.setStyleSheet("background-color: #3d3d3d")
        self.ui.buttonSecurity.setStyleSheet("")
        self.ui.stackedWidget.setCurrentWidget(self.ui.widgetGenerate)

    def show_security(self):
        """Highlights the 'Security Check' tab."""
        self.ui.buttonPasswords.setStyleSheet("")
        self.ui.buttonAddNew.setStyleSheet("")
        self.ui.buttonGenerate.setStyleSheet("")
        self.ui.buttonSecurity.setStyleSheet("background-color: #3d3d3d")
        self.ui.stackedWidget.setCurrentWidget(self.ui.widgetSecurity)

    # ----- Password Dashboard -----
    def update_table(self):
        """Inserts the data from the 'Add New' form into the passwords table."""
        data = [
            self.ui.editTitle.text(),
            self.ui.editUsername.text(),
            self.ui.editUrl.text(),
            "".join(["*" for i in self.ui.editPassword.text()]),
        ]

        total_rows = self.ui.tablePasswords.rowCount()

        for i in range(3):
            self.ui.tablePasswords.setItem(
                total_rows, i, QTableWidgetItem(data[i])
            )

        print(f"Total rows: {total_rows}")

    # ----- Add New -----
    def update_db(self):
        """Inserts the data from the 'Add New' form into the database."""
        self.db = SqliteCipher(
            dataBasePath="Password_Vault.db",
            checkSameThread=True,
            password=keyring_get_password("Password Vault", "user"),
        )
        if not self.db.checkTableExist("Password"):
            self.db.createTable(
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
        self.db.insertIntoTable(
            tableName="Password",
            insertList=[
                self.ui.editTitle.text(),
                self.ui.editUrl.text(),
                self.ui.editUsername.text(),
                self.ui.editPassword.text(),
                self.is_password_compromised(self.ui.editPassword.text()),
            ],
            commit=True,
        )

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
            self.dlg_none_selected.exec()

    def copy_generated_pwd(self):
        copy(self.ui.labelGeneratedPwd.text())
        self.ui.labelCopiedToClip.setText("Copied to clipboard.")
