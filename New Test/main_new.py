from qdarktheme import load_stylesheet
from sys import exit as sys_exit
from os import system
from os.path import exists
from password_strength import PasswordStats
from pwnedpasswords import check as check_pwned
from pyperclip import copy as copy_to_cb
from pysqlcipher3 import dbapi2 as sqlcipher
from secrets import choice as secrets_choice
from string import ascii_uppercase, ascii_lowercase, digits
from validators import url as is_url_valid

from PySide6.QtCore import (
    QRect,
    Signal,
    Qt,
    QSortFilterProxyModel,
    QModelIndex,
)
from PySide6.QtGui import QStandardItemModel, QStandardItem, QIcon
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QTableWidgetItem,
    QMessageBox,
    QLineEdit,
    QTableView,
    QHeaderView,
    QApplication,
    QStackedLayout,
)

system("pyside6-uic log_in.ui > ui_log_in.py")
from ui_log_in import Ui_MainWindow as Ui_LogInWindow

system("pyside6-uic main_window.ui > ui_main_window.py")
from ui_main_window import Ui_MainWindow


class LogInWindow(QMainWindow):
    logged_in = Signal()

    def __init__(self, db):
        super(LogInWindow, self).__init__()
        self.db = db

        self.ui = Ui_LogInWindow()
        self.ui.setupUi(self)

        self.setFixedWidth(340)
        self.setFixedHeight(370)

        self.ui.editPasswordMain.setFocus()

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
                self.is_table_created = self.db.execute(
                    "SELECT name FROM sqlite_master WHERE type='table' AND name='Passwords';"
                ).fetchall()
            except db.DatabaseError:
                self.is_table_created = True

        if self.is_table_created:
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
        self.ui.editPasswordMain.returnPressed.connect(self.log_in)
        self.ui.editPasswordConfirm.returnPressed.connect(self.log_in)
        self.ui.buttonPasswordToggle1.clicked.connect(self.toggle_view1)
        self.ui.buttonPasswordToggle2.clicked.connect(self.toggle_view2)
        self.ui.buttonSubmit.clicked.connect(self.log_in)
        # ----------------------------------------------------------

    def log_in(self):
        if self.is_table_created:
            self.enter_master_password()
        else:
            self.create_master_password()

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
            with self.db:
                self.db.execute(
                    f'PRAGMA key=":{self.ui.editPasswordMain.text()}"'
                )
                self.db.execute(
                    """
                    CREATE TABLE IF NOT EXISTS Passwords (
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
                return self.ui.editPasswordMain.text()

    def enter_master_password(self):
        if len(self.ui.editPasswordMain.text()) > 0:
            with db:
                db.execute(
                    f"PRAGMA key={self.ui.editPasswordMain.text()}",
                )
                try:
                    db.execute("SELECT count(*) FROM sqlite_master;")
                    self.logged_in.emit()
                except sqlcipher.DatabaseError:
                    self.dlg_incorrect_password()
        else:
            self.dlg_incorrect_password()

    def toggle_view1(self, checked):
        if checked:
            self.ui.editPasswordMain.setEchoMode(QLineEdit.EchoMode.Normal)
            self.ui.buttonPasswordToggle1.setIcon(QIcon("icons/eye.svg"))
        else:
            self.ui.editPasswordMain.setEchoMode(QLineEdit.EchoMode.Password)
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


class MainWindow(QMainWindow):
    def __init__(self, db):
        super(MainWindow, self).__init__()
        self.db = db
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setFixedWidth(800)
        self.setFixedHeight(600)

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
            buttons=QMessageBox.Yes | QMessageBox.No,
        )
        self.dlg_invalid_url = lambda: QMessageBox.critical(
            self,
            "Password Manager",
            "Error: URL is invalid.",
            buttons=QMessageBox.Ok,
        )
        self.dlg_log_out_confirmation = lambda: QMessageBox.question(
            self,
            "Password Manager",
            "Are you sure you want to log out?",
            buttons=QMessageBox.Yes | QMessageBox.Cancel,
        )
        # -------------------------

        # ----- Side-Menu -----
        self.ui.stackedWidget.setCurrentWidget(self.ui.widgetPasswords)
        self.ui.buttonTabPasswords.setStyleSheet(
            "background-color: #3d3d3d; border-left: 3px solid #8ab4f7"
        )
        self.ui.buttonTabPasswords.clicked.connect(self.show_passwords_tab)
        self.ui.buttonTabPasswords.clicked.connect(self.update_dashboard_table)
        self.ui.buttonTabAddNew.clicked.connect(self.show_add_new_tab)
        self.ui.buttonTabGenerate.clicked.connect(self.show_generate_tab)
        self.ui.buttonTabHealth.clicked.connect(self.show_health_tab)
        self.generate_password()
        self.ui.buttonLogOut.clicked.connect(self.log_out)

        # ----- Password Dashboard ----------------
        self.ui.buttonDelete.clicked.connect(self.delete_password)
        self.ui.buttonCopyPassword.clicked.connect(self.copy_password)
        # ------------------------------------------

        # ----- Add New -----
        self.ui.buttonAddPassword.clicked.connect(self.update_db)
        self.ui.editUrl.returnPressed.connect(self.update_db)
        self.ui.editUsername.returnPressed.connect(self.update_db)
        self.ui.editPassword.returnPressed.connect(self.update_db)
        self.ui.buttonPasswordToggle.clicked.connect(self.password_toggle)
        self.ui.comboBoxTitle.currentTextChanged.connect(self.set_url)
        self.ui.comboBoxTitle.currentIndexChanged.connect(self.set_url)

        # ----- Generate Password -----
        self.ui.horizontalSlider.valueChanged.connect(self.update_spin_box)
        self.ui.spinBox.valueChanged.connect(self.update_slider)
        self.ui.horizontalSlider.valueChanged.connect(self.generate_password)
        self.ui.spinBox.valueChanged.connect(self.generate_password)
        self.ui.checkBoxUpper.clicked.connect(self.generate_password)
        self.ui.checkBoxLower.clicked.connect(self.generate_password)
        self.ui.checkBoxDigits.clicked.connect(self.generate_password)
        self.ui.checkBoxSymbols.clicked.connect(self.generate_password)
        self.ui.buttonRegenerate.clicked.connect(self.generate_password)
        self.ui.buttonCopyRandomPassword.clicked.connect(
            self.copy_generated_pwd
        )
        self.ui.checkBoxUpper.clicked.connect(self.disable_check_box)
        self.ui.checkBoxLower.clicked.connect(self.disable_check_box)
        self.ui.checkBoxDigits.clicked.connect(self.disable_check_box)
        self.ui.checkBoxSymbols.clicked.connect(self.disable_check_box)

        # ----- Password Health -----
        self.ui.buttonTabHealth.clicked.connect(self.update_health_stats)

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

    def db_create_passwords_table(self):
        db.createTable(
            "Password",
            [
                ["name", "TEXT"],
                ["url", "TEXT"],
                ["username", "TEXT"],
                ["password", "TEXT"],
                ["isCompromised", "INT"],
                ["strength", "TEXT"],
            ],
            makeSecure=True,
        )

    # ----- Password Dashboard -----
    def update_dashboard_table(self):
        """Inserts the data from the database into the passwords table."""
        data = self.get_db_data()

        model = QStandardItemModel(len(data), 3)
        model.setHorizontalHeaderLabels(
            ["Name", "URL", "Username", "Password"]
        )

        for row_num in range(len(data)):
            for col_num, col_data in enumerate(data[row_num]):
                if col_num == 3:  # Store password in symbol '*'.
                    col_data = "".join("*" for i in range(len(col_data)))
                elif col_num == 4:
                    break
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
        try:
            selected_name = self.ui.tablePasswords.selectedIndexes()[0].data()
            db_data = db.get_db_data()
            db_data_names = list(list(zip(*db_data))[0])
            id_to_delete = db_data_names.index(selected_name)
            if self.dlg_delete_confirmation() == QMessageBox.Yes:
                db.deleteDataInTable("Password", id_to_delete)
                self.update_dashboard_table()
        except IndexError:
            self.dlg_no_password_selected()

    def edit_password(self):
        pass

    def copy_password(self):
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
        """
        Inserts the data from the 'Add New' form, along with password
        statistics into the database.
        """
        form_data = [
            self.ui.comboBoxTitle.currentText(),
            self.ui.editUrl.text().lower(),
            self.ui.editUsername.text(),
            self.ui.editPassword.text(),
            self.is_password_compromised(self.ui.editPassword.text()),
            self.get_password_strength(self.ui.editPassword.text()),
        ]

        # Check if all fields in the form are filled.
        if sum(1 if i != "" else 0 for i in form_data) != len(form_data):
            self.dlg_form_not_filled()
        # Check if URL is valid.
        elif self.ui.editUrl.text().replace(
            " ", ""
        ) != "" and not is_url_valid(self.ui.editUrl.text().lower()):
            self.dlg_invalid_url()
        elif (
            False
        ):  # TODO: Check if name entered already exists in table/database
            pass
        else:
            db.insertIntoTable(
                tableName="Password",
                insertList=form_data,
            )
            self.dlg_pwd_added()
            self.clear_password_form()

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
            1 if check_pwned(password, plain_text=True, anonymous=True) else 0
        )

    # ----- Generate Password -----
    def update_spin_box(self):
        self.ui.spinBox.setValue(self.ui.horizontalSlider.value())

    def update_slider(self):
        self.ui.horizontalSlider.setValue(self.ui.spinBox.value())

    def generate_password(self):
        len = self.ui.spinBox.value()

        characters = ""
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

    def disable_check_box(self):
        """
        Disables the check box that is checked when only one of the boxes are
        checked.
        """
        check_boxes_list = [
            self.ui.checkBoxUpper,
            self.ui.checkBoxLower,
            self.ui.checkBoxDigits,
            self.ui.checkBoxSymbols,
        ]
        boxes_checked = [
            check_box.isChecked()
            for check_box_num, check_box in enumerate(check_boxes_list)
        ]

        if sum(boxes_checked) == 1:
            check_box_checked = boxes_checked.index(True)
            check_boxes_list[check_box_checked].setEnabled(False)
        else:
            for check_box in check_boxes_list:
                check_box.setEnabled(True)

    def get_db_data(self):
        if not db.checkTableExist("Password"):
            self.db_create_passwords_table()
        return db.getDataFromTable(
            "Password", raiseConversionError=True, omitID=True
        )[1:][0]

    def update_health_stats(self):
        data = self.get_db_data()

        if len(data) > 0:
            security_score = self.get_security_score(list(list(zip(*data))[3]))
            self.ui.labelSecurityScore.setText(f"{str(security_score)}%")

            total_unique = len(set(list(list(zip(*data))[3])))
            total_reused = len(data) - total_unique
            self.ui.labelReused.setText(str(total_reused))

            total_passwords = len(data)
            self.ui.labelTotalPasswords.setText(str(total_passwords))

            total_compromised = len(
                [i for i in [data[i][4] for i in range(len(data))] if i == 1]
            )
            self.ui.labelCompromised.setText(str(total_compromised))

            total_weak = len(
                [
                    i
                    for i in [data[i][5] for i in range(len(data))]
                    if i == "weak" or i == "medium"
                ]
            )
            self.ui.labelWeak.setText(str(total_weak))

            total_safe = len(
                [
                    i
                    for i in [data[i][5] for i in range(len(data))]
                    if i == "strong"
                ]
            )
            self.ui.labelSafe.setText(str(total_safe))

    def set_url(self):
        url_list = [
            "",
            "https://www.alibaba.com",
            "https://www.aliexpress.com",
            "https://www.amazon.com",
            "https://www.bing.com",
            "https://www.cash.app",
            "https://www.discord.com",
            "https://www.ebay.com",
            "https://www.facebook.com",
            "https://www.flipkart.com",
            "https://www.foodpanda.com",
            "https://www.google.com",
            "https://www.instagram.com",
            "https://www.linkedin.com",
            "https://www.mcdonalds.com",
            "https://www.netflix.com",
            "https://www.reddit.com",
            "https://www.shopee.com",
            "https://www.snapchat.com",
            "https://www.spotify.com",
            "https://www.starbucks.com",
            "https://www.telegram.com",
            "https://www.tiktok.com",
            "https://www.twitch.com",
            "https://www.twitter.com",
            "https://www.uber.com",
            "https://www.wechat.com",
            "https://www.whatsapp.com",
            "https://www.wish.com",
            "https://www.wolt.com",
            "https://www.yahoo.com",
            "https://www.zoom.com",
        ]
        try:
            title_selected = self.ui.comboBoxTitle.currentIndex()
            self.ui.editUrl.setText(url_list[title_selected])
        except IndexError:
            self.ui.editUrl.setText("")

    def clear_password_form(self):
        self.ui.comboBoxTitle.setCurrentIndex(0)
        self.ui.editUsername.clear()
        self.ui.editUrl.clear()
        self.ui.editPassword.clear()

    def log_out(self):
        if self.dlg_log_out_confirmation() == QMessageBox.Yes:
            sys_exit()

    def get_password_strength(self, password):
        if len(password) > 0:
            score = PasswordStats(password).strength()
            if score >= 0 and score < 0.33:
                return "weak"
            elif score >= 0.33 and score < 0.66:
                return "medium"
            elif score >= 0.66:
                return "strong"

    def get_security_score(self, password_list):
        score = [
            PasswordStats(password).strength() for password in password_list
        ]
        return int(sum(score) / len(password_list) * 100)


def main():
    app = QApplication([])
    app.setStyleSheet(load_stylesheet("dark", "rounded"))

    db = sqlcipher.connect("New Test/passwordManager.db")

    layout = QStackedLayout()

    log_in_window = LogInWindow(db)
    layout.addWidget(log_in_window)

    layout.setCurrentWidget(log_in_window)

    main_window = MainWindow(db)
    layout.addWidget(main_window)

    log_in_window.logged_in.connect(
        lambda w=main_window: layout.setCurrentWidget(w)
    )
    sys_exit(app.exec())


if __name__ == "__main__":
    main()
