from bcrypt import hashpw, gensalt
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

        self.setFixedWidth(340)
        self.setFixedHeight(370)

        self.ui.editPasswordMain.setFocus()

        # -------- Creating the error dialogue boxes. --------
        self.dlg_password_short = lambda: QMessageBox.warning(
            self,
            "Password Manager",
            "The master password must contain at least 8 characters.",
            buttons=QMessageBox.Ok,
        )
        self.dlg_passwords_not_match = lambda: QMessageBox.warning(
            self,
            "Password Manager",
            "Master passwords do not match.",
            buttons=QMessageBox.Ok,
        )
        self.dlg_empty_password = lambda: QMessageBox.warning(
            self,
            "Password Manager",
            "Make sure to fill both fields.",
            buttons=QMessageBox.Ok,
        )
        self.dlg_password_created = lambda: QMessageBox.information(
            self,
            "Password Manager",
            "Your master password has been created successfully.",
            buttons=QMessageBox.Ok,
        )
        self.dlg_incorrect_password = lambda: QMessageBox.warning(
            self,
            "Password Manager",
            "Incorrect master password. Please try again.",
            buttons=QMessageBox.Ok,
        )
        # --------------------------------------------------

        if exists("Password_Manager.db"):
            self.setFixedHeight(280)
            self.ui.labelHeading.setText("Enter Master Password")
            self.ui.labelSubHeading.setText(
                "Enter the master password to access your password vault."
            )
            self.ui.groupBoxMain.hide()
            self.ui.groupBoxConfirm.setGeometry(40, 130, 260, 60)
            self.ui.groupBoxConfirm.setTitle("Master password")
            self.ui.buttonSubmit.setText("Unlock")
            self.ui.buttonSubmit.setGeometry(QRect(40, 210, 250, 27))

        # ---- Connecting user actions to the appropriate functions.
        self.ui.buttonSubmit.clicked.connect(self.log_in)
        self.ui.editPasswordMain.returnPressed.connect(self.log_in)
        self.ui.buttonPasswordToggle1.setCheckable(True)
        self.ui.buttonPasswordToggle1.clicked.connect(self.password_toggle1)
        self.ui.editPasswordConfirm.returnPressed.connect(self.log_in)
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
            self.ui.editPasswordMain.setEchoMode(QLineEdit.EchoMode.Normal)
            self.ui.buttonPasswordToggle1.setIcon(QIcon("icons/eye.svg"))
        else:
            self.ui.editPasswordMain.setEchoMode(QLineEdit.EchoMode.Password)
            self.ui.buttonPasswordToggle1.setIcon(
                QIcon("icons/eye-crossed.svg")
            )

    def password_toggle2(self, checked):
        if checked:
            self.ui.editPasswordConfirm.setEchoMode(QLineEdit.EchoMode.Normal)
            self.ui.buttonPasswordToggle2.setIcon(QIcon("icons/eye.svg"))
        else:
            self.ui.editPasswordConfirm.setEchoMode(
                QLineEdit.EchoMode.Password
            )
            self.ui.buttonPasswordToggle2.setIcon(
                QIcon("icons/eye-crossed.svg")
            )

    def create_master_password(self):
        if (
            len(self.ui.editPasswordMain.text()) == 0
            or len(self.ui.editPasswordConfirm.text()) == 0
        ):
            self.dlg_empty_password()
        elif (
            self.ui.editPasswordMain.text()
            != self.ui.editPasswordConfirm.text()
        ):
            self.dlg_passwords_not_match()
        elif (
            len(self.ui.editPasswordMain.text()) < 8
            and len(self.ui.editPasswordMain.text()) < 8
        ):
            self.dlg_password_short()
        else:
            print(hashpw(self.ui.editPasswordMain.text().encode(), gensalt()))
            self.db = SqliteCipher(
                dataBasePath="Password_Manager.db",
                checkSameThread=True,
                password=(self.ui.editPasswordMain.text()),
            )
            keyring_set_password(
                "Password Manager",
                "user",
                hashpw(self.ui.editPasswordMain.text().encode(), gensalt()),
            )
            self.dlg_password_created()
            self.logged_in.emit()

    def enter_master_password(self):
        if len(
            self.ui.editPasswordConfirm.text()
        ) == 0 or SqliteCipher.sha512Convertor(
            self.ui.editPasswordConfirm.text()
        ) != SqliteCipher.getVerifier(
            "Password_Manager.db", checkSameThread=True
        ):
            self.dlg_incorrect_password()
        else:
            self.logged_in.emit()
