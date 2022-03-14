from os.path import exists
from keyring import (
    set_password as keyring_set_password,
    delete_password as keyring_delete_password,
    get_password as keyring_get_password,
)
from pysqlcipher3 import dbapi2 as sqlcipher

from PySide6.QtCore import QRect, Signal
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QMainWindow, QMessageBox, QLineEdit

from ui_log_in import Ui_MainWindow


class LogInWindow(QMainWindow):
    logged_in = Signal()

    def __init__(self, db):
        super(LogInWindow, self).__init__()
        self.db = db

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setFixedWidth(340)
        self.setFixedHeight(370)

        self.ui.editPassword.setFocus()

        # -------- Creating the error dialogue boxes.
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
        # -------------------------------------------

        with self.db:
            try:
                self.is_master_pass_created = self.db.execute(
                    "SELECT name FROM sqlite_master WHERE type='table' AND name='Passwords';"
                ).fetchall()
            except db.DatabaseError:
                self.is_master_pass_created = True

        if self.is_master_pass_created:
            self.setFixedHeight(310)
            self.ui.labelHeading.setText("Enter Master Password")
            self.ui.labelSubHeading.setText(
                "Enter the master password to access your password vault."
            )
            self.ui.groupBoxConfirm.hide()
            self.ui.groupBoxConfirm.setGeometry(40, 130, 260, 60)
            self.ui.groupBoxConfirm.setTitle("Master password")
            self.ui.buttonCreate.setText("Unlock")
            self.ui.buttonCreate.setGeometry(QRect(40, 245, 260, 27))

        # ---- Connecting user actions to the appropriate functions.
        self.ui.editPassword.returnPressed.connect(self.log_in)
        self.ui.editPasswordConfirm.returnPressed.connect(self.log_in)
        self.ui.buttonPasswordToggle1.setCheckable(True)
        self.ui.buttonPasswordToggle1.clicked.connect(self.toggle_view1)
        self.ui.buttonPasswordToggle2.setCheckable(True)
        self.ui.buttonPasswordToggle2.clicked.connect(self.toggle_view2)
        self.ui.buttonCreate.clicked.connect(self.log_in)
        # ----------------------------------------------------------

    def log_in(self):
        if self.is_master_pass_created:
            self.is_master_password_correct()
        else:
            self.create_master_password()

    def is_master_password_correct(self):
        with self.db:
            try:
                self.db.execute(f"PRAGMA key='{self.ui.editPassword.text()}';")
                self.db.execute(
                    "SELECT count(*) FROM sqlite_master;"
                ).fetchall()
                self.logged_in.emit()
            except sqlcipher.DatabaseError:
                self.dlg_incorrect_password()

    def create_master_password(self):
        if (
            len(self.ui.editPassword.text()) == 0
            or len(self.ui.editPasswordConfirm.text()) == 0
        ):
            self.dlg_empty_password()
        elif self.ui.editPassword.text() != self.ui.editPasswordConfirm.text():
            self.dlg_passwords_not_match()
        elif (
            len(self.ui.editPassword.text()) < 8
            and len(self.ui.editPasswordConfirm.text()) < 8
        ):
            self.dlg_password_short()
        else:
            with self.db:
                self.db.execute(
                    f"PRAGMA key='{self.ui.editPassword.text()}';",
                )
                self.db.execute(
                    """
                    CREATE TABLE Passwords (
                        id INTEGER PRIMARY KEY,
                        name TEXT,
                        username TEXT,
                        password TEXT,
                        isCompromised BIT,
                        passwordStrength TEXT
                    );
                    """
                )
                self.dlg_password_created()
                self.logged_in.emit()

    def toggle_view1(self, checked):
        if checked:
            self.ui.editPassword.setEchoMode(QLineEdit.EchoMode.Normal)
            self.ui.buttonPasswordToggle1.setIcon(QIcon("icons/eye.svg"))
        else:
            self.ui.editPassword.setEchoMode(QLineEdit.EchoMode.Password)
            self.ui.buttonPasswordToggle1.setIcon(
                QIcon("icons/eye-crossed.svg")
            )

    def toggle_view2(self, checked):
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
