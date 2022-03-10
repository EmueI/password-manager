from os.path import exists
from keyring import (
    set_password as keyring_set_password,
    delete_password as keyring_delete_password,
    get_password as keyring_get_password,
)
from pysqlitecipher.sqlitewrapper import SqliteCipher

from PySide6.QtCore import QRect, Signal
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QMainWindow, QMessageBox, QLineEdit

from ui_log_in import Ui_MainWindow


class MainWindow(QMainWindow):
    logged_in = Signal()

    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setFixedWidth(320)
        self.setFixedHeight(370)

        self.ui.editPassword1.setFocus()

        # -------- Creating the error dialogue boxes. --------
        self.dlg_password_short = QMessageBox(self)
        self.dlg_password_short.setWindowTitle("Password Manager")
        self.dlg_password_short.setText(
            "The master password must contain at least 8 characters."
        )
        self.dlg_password_short.setStandardButtons(QMessageBox.Ok)
        self.dlg_password_short.setIcon(QMessageBox.Warning)

        self.dlg_passwords_not_match = QMessageBox(self)
        self.dlg_passwords_not_match.setWindowTitle("Password Manager")
        self.dlg_passwords_not_match.setText("Master passwords do not match.")
        self.dlg_passwords_not_match.setStandardButtons(QMessageBox.Ok)
        self.dlg_passwords_not_match.setIcon(QMessageBox.Warning)

        self.dlg_empty_password = QMessageBox(self)
        self.dlg_empty_password.setWindowTitle("Password Manager")
        self.dlg_empty_password.setText("Make sure to fill both boxes.")
        self.dlg_empty_password.setStandardButtons(QMessageBox.Ok)
        self.dlg_empty_password.setIcon(QMessageBox.Warning)

        self.dlg_password_created = QMessageBox(self)
        self.dlg_password_created.setWindowTitle("Password Manager")
        self.dlg_password_created.setText(
            "Your master password has been created successfully."
        )
        self.dlg_password_created.setStandardButtons(QMessageBox.Ok)
        self.dlg_password_created.setIcon(QMessageBox.Information)

        self.dlg_incorrect_password = QMessageBox(self)
        self.dlg_incorrect_password.setWindowTitle("Password Manager")
        self.dlg_incorrect_password.setText(
            "Incorrect master password. Please try again."
        )
        self.dlg_incorrect_password.setStandardButtons(QMessageBox.Ok)
        self.dlg_incorrect_password.setIcon(QMessageBox.Warning)
        # --------------------------------------------------

        if exists("Password_Manager.db"):
            self.setFixedHeight(255)
            self.ui.labelHeading.setText("Enter Master Password")
            self.ui.labelSubHeading.setText(
                "Enter the master password to access your password vault."
            )
            self.ui.labelPassword1.hide()
            self.ui.labelPassword1Sub.hide()
            self.ui.frameMainPwd1.setGeometry(QRect(40, 130, 250, 31))
            self.ui.frameMainPwd2.hide()
            self.ui.buttonSubmit.setText("Unlock")
            self.ui.buttonSubmit.setGeometry(QRect(40, 185, 250, 27))

        # ---- Connecting user actions to the appropriate functions.
        self.ui.buttonSubmit.clicked.connect(self.log_in)
        self.ui.editPassword1.returnPressed.connect(self.log_in)
        self.ui.buttonPasswordToggle1.setCheckable(True)
        self.ui.buttonPasswordToggle1.clicked.connect(self.password_toggle1)
        self.ui.editPassword2.returnPressed.connect(self.log_in)
        self.ui.buttonPasswordToggle2.setCheckable(True)
        self.ui.buttonPasswordToggle2.clicked.connect(self.password_toggle2)
        # -----------------------------------------------------------

    def log_in(self):
        if exists("Password_Manager.db"):
            self.enter_master_password()
        else:
            self.create_master_password()

    def password_toggle1(self, checked):
        if checked:
            self.ui.editPassword1.setEchoMode(QLineEdit.EchoMode.Normal)
            self.ui.buttonPasswordToggle1.setIcon(QIcon("icons/eye.svg"))
        else:
            self.ui.editPassword1.setEchoMode(QLineEdit.EchoMode.Password)
            self.ui.buttonPasswordToggle1.setIcon(
                QIcon("icons/eye-crossed.svg")
            )

    def password_toggle2(self, checked):
        if checked:
            self.ui.editPassword2.setEchoMode(QLineEdit.EchoMode.Normal)
            self.ui.buttonPasswordToggle2.setIcon(QIcon("icons/eye.svg"))
        else:
            self.ui.editPassword2.setEchoMode(QLineEdit.EchoMode.Password)
            self.ui.buttonPasswordToggle2.setIcon(
                QIcon("icons/eye-crossed.svg")
            )

    def create_master_password(self):
        if (
            len(self.ui.editPassword1.text()) == 0
            or len(self.ui.editPassword2.text()) == 0
        ):
            self.dlg_empty_password.exec()
        elif self.ui.editPassword1.text() != self.ui.editPassword2.text():
            self.dlg_passwords_not_match.exec()
        elif (
            len(self.ui.editPassword1.text()) < 8
            and len(self.ui.editPassword1.text()) < 8
        ):
            self.dlg_password_short.exec()
        else:
            self.db = SqliteCipher(
                dataBasePath="Password_Manager.db",
                checkSameThread=True,
                password=(self.ui.editPassword1.text()),
            )
            keyring_set_password(
                "Password Manager",
                "user",
                self.ui.editPassword1.text(),
            )
            self.dlg_password_created.exec()
            self.logged_in.emit()

    def enter_master_password(self):
        if len(
            self.ui.editPassword1.text()
        ) == 0 or SqliteCipher.sha512Convertor(
            self.ui.editPassword1.text()
        ) != SqliteCipher.getVerifier(
            "Password_Manager.db", checkSameThread=True
        ):
            self.dlg_incorrect_password.exec()
        else:
            self.logged_in.emit()
