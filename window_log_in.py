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

        with self.db:
            try:
                self.is_master_pass_created = self.db.execute(
                    "SELECT name FROM sqlite_master WHERE type='table' AND name='Password';"
                ).fetchall()
            except sqlcipher.DatabaseError:
                self.is_master_pass_created = True

        if self.is_master_pass_created:
            self.setFixedHeight(290)
            self.ui.labelHeading.setText("Enter Master Password")
            self.ui.labelSubHeading.setText(
                "Enter the master password to access your password vault."
            )
            self.ui.label.deleteLater()
            self.ui.groupBox.setFixedHeight(70)
            self.ui.groupBoxConfirm.hide()
            self.ui.groupBoxConfirm.setGeometry(40, 130, 260, 60)
            self.ui.groupBoxConfirm.setTitle("Master password")
            self.ui.button.setText("Unlock")
            self.ui.button.setGeometry(QRect(40, 225, 260, 27))

        # ---- Connecting user actions to the appropriate functions.
        self.ui.editPassword.returnPressed.connect(self.log_in)
        self.ui.editPasswordConfirm.returnPressed.connect(self.log_in)
        self.ui.buttonPasswordToggle1.setCheckable(True)
        self.ui.buttonPasswordToggle1.clicked.connect(self.toggle_view1)
        self.ui.buttonPasswordToggle2.setCheckable(True)
        self.ui.buttonPasswordToggle2.clicked.connect(self.toggle_view2)
        self.ui.button.clicked.connect(self.log_in)
        # ----------------------------------------------------------

    def log_in(self):
        if self.is_master_pass_created:
            self.check_master_pass_input()
        else:
            self.create_master_password()

    def check_master_pass_input(self):
        with self.db:
            try:
                self.db.execute(f"PRAGMA key='{self.ui.editPassword.text()}';")
                self.db.execute("SELECT count(*) FROM sqlite_master;")
                self.logged_in.emit()
            except sqlcipher.DatabaseError:
                QMessageBox.warning(
                    self,
                    "Password Manager",
                    "Incorrect master password. Please try again.",
                )

    def create_master_password(self):
        if (
            len(self.ui.editPassword.text()) == 0
            or len(self.ui.editPasswordConfirm.text()) == 0
        ):
            QMessageBox.warning(
                self,
                "Password Manager",
                "Confirmation does not match or is empty.",
            )
        elif self.ui.editPassword.text() != self.ui.editPasswordConfirm.text():
            QMessageBox.warning(
                self,
                "Password Manager",
                "Master passwords do not match.",
            )
        elif (
            len(self.ui.editPassword.text()) < 8
            and len(self.ui.editPasswordConfirm.text()) < 8
        ):
            QMessageBox.warning(
                self,
                "Password Manager",
                "Your master password must contain at least 8 characters.",
            )
        else:
            with self.db:
                self.db.execute(
                    f"PRAGMA key='{self.ui.editPassword.text()}';",
                )
                self.db.execute(
                    """
                    CREATE TABLE IF NOT EXISTS Password (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT,
                        url TEXT,
                        username TEXT,
                        password TEXT,
                        isCompromised INTEGER,
                        passwordStrength TEXT
                    );
                    """
                )
                QMessageBox.information(
                    self,
                    "Password Manager",
                    "Your master password has been created successfully.",
                )
                self.logged_in.emit()

    def toggle_view1(self, checked):
        self.ui.editPassword.setEchoMode(
            QLineEdit.EchoMode.Normal
            if checked
            else QLineEdit.EchoMode.Password
        )
        self.ui.buttonPasswordToggle1.setIcon(
            QIcon("icons/eye.svg")
            if checked
            else QIcon("icons/eye-crossed.svg")
        )

    def toggle_view2(self, checked):
        self.ui.editPasswordConfirm.setEchoMode(
            QLineEdit.EchoMode.Normal
            if checked
            else QLineEdit.EchoMode.Password
        )
        self.ui.buttonPasswordToggle2.setIcon(
            QIcon("icons/eye.svg")
            if checked
            else QIcon("icons/eye-crossed.svg")
        )
