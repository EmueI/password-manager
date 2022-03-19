import urllib.request

from password_strength import PasswordStats
from pwnedpasswords import check as check_pwned
from pyperclip import copy as copy_to_cb
from pysqlcipher3 import dbapi2 as sqlcipher
from secrets import choice as secrets_choice
from string import ascii_uppercase, ascii_lowercase, digits
from sys import exit as sys_exit
from validators import url as is_url_valid

from PySide6.QtCore import Qt, QSortFilterProxyModel
from PySide6.QtWidgets import (
    QMainWindow,
    QMessageBox,
    QLineEdit,
)
from PySide6.QtGui import QStandardItemModel, QStandardItem, QIcon

from ui_main_window import Ui_MainWindow


class MainWindow(QMainWindow):
    def __init__(self, db):
        super(MainWindow, self).__init__()
        self.db = db
        if not self.is_access_granted():
            QMessageBox.critical(
                self,
                "Password Manager",
                "Access denied.",
            )
            sys_exit()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setFixedWidth(800)
        self.setFixedHeight(600)

        # ----- Message Boxes -----
        self.dlg_no_row_selected = lambda: QMessageBox.warning(
            self,
            "Password Manager",
            "No password selected.",
        )
        self.dlg_delete_confirmation = lambda: QMessageBox.question(
            self,
            "Password Manager",
            "Are you sure you want to delete this password?",
            buttons=QMessageBox.Yes | QMessageBox.No,
        )
        self.dlg_log_out_confirm = lambda: QMessageBox.question(
            self,
            "Password Manager",
            "Are you sure you want to log out?",
            buttons=QMessageBox.Yes | QMessageBox.Cancel,
        )
        # -------------------------

        self.filter_proxy_model = QSortFilterProxyModel()
        self.filter_proxy_model.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.filter_proxy_model.setFilterKeyColumn(0)

        self.ui.tablePasswords.setModel(self.filter_proxy_model)
        self.ui.editSearch.textChanged.connect(
            self.filter_proxy_model.setFilterRegularExpression
        )

        # ----- Side-Menu -----
        self.ui.stackedWidget.setCurrentWidget(self.ui.widgetPasswords)
        self.ui.buttonTabPasswords.setStyleSheet(
            "background-color: #3d3d3d; border-left: 3px solid #8ab4f7"
        )
        self.ui.buttonTabPasswords.clicked.connect(self.show_passwords_tab)
        self.update_dashboard_table()
        self.ui.buttonTabAddNew.clicked.connect(self.show_add_new_tab)
        self.ui.buttonTabGenerate.clicked.connect(self.show_generate_tab)
        self.ui.buttonTabHealth.clicked.connect(self.show_health_tab)
        self.ui.buttonLogOut.clicked.connect(self.log_out)

        # ----- Password Dashboard ----------------
        self.ui.buttonDelete.clicked.connect(self.delete_password)
        self.ui.buttonCopyPassword.clicked.connect(self.copy_password)

        # ----- Add New -----
        self.ui.buttonTabPasswords.clicked.connect(self.update_dashboard_table)
        self.ui.buttonAddPassword.clicked.connect(self.update_db)
        self.ui.editEntryUrl.returnPressed.connect(self.update_db)
        self.ui.editEntryUsername.returnPressed.connect(self.update_db)
        self.ui.editEntryPassword.returnPressed.connect(self.update_db)
        self.ui.editEntryPasswordConfirm.returnPressed.connect(self.update_db)
        self.ui.buttonPasswordToggle.clicked.connect(self.password_toggle)
        self.ui.buttonPasswordToggle2.clicked.connect(
            self.password_confirm_toggle
        )
        self.ui.comboBoxEntryTitle.currentTextChanged.connect(self.set_url)
        self.ui.comboBoxEntryTitle.currentIndexChanged.connect(self.set_url)

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
        self.generate_password()

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
        self.ui.buttonTabAddNew.setStyleSheet(
            "background-color: #3d3d3d; border-left: 4px solid #8ab4f7"
        )
        self.ui.buttonTabPasswords.setStyleSheet("")
        self.ui.buttonTabGenerate.setStyleSheet("")
        self.ui.buttonTabHealth.setStyleSheet("")
        self.ui.stackedWidget.setCurrentWidget(self.ui.widgetAdd)

    def show_generate_tab(self):
        """Highlights the 'Generate Passwords' tab."""
        self.ui.buttonTabGenerate.setStyleSheet(
            "background-color: #3d3d3d; border-left: 4px solid #8ab4f7"
        )
        self.ui.buttonTabPasswords.setStyleSheet("")
        self.ui.buttonTabAddNew.setStyleSheet("")
        self.ui.buttonTabHealth.setStyleSheet("")
        self.ui.stackedWidget.setCurrentWidget(self.ui.widgetGenerate)

    def show_health_tab(self):
        """Highlights the 'Health Check' tab."""
        self.ui.buttonTabHealth.setStyleSheet(
            "background-color: #3d3d3d; border-left: 4px solid #8ab4f7"
        )
        self.ui.buttonTabPasswords.setStyleSheet("")
        self.ui.buttonTabAddNew.setStyleSheet("")
        self.ui.buttonTabGenerate.setStyleSheet("")
        self.ui.stackedWidget.setCurrentWidget(self.ui.widgetHealth)

    # ----- Passwords Dashboard -----
    def update_dashboard_table(self):
        """Inserts the data from the database into the dashboard's passwords table."""
        data = self.db.execute(
            "SELECT name, url, username, password FROM Password"
        ).fetchall()

        model = QStandardItemModel(len(data), 3)
        model.setHorizontalHeaderLabels(
            ["Name", "URL", "Username", "Password"]
        )
        for row_index, row in enumerate(data):
            for col_index, col_data in enumerate(row):
                if col_index == 3:
                    col_data = "*" * len(col_data)
                model.setItem(row_index, col_index, QStandardItem(col_data))
        self.filter_proxy_model.setSourceModel(model)

    def delete_password(self):
        """Removes the selected row from the database."""
        try:
            selected_name = self.ui.tablePasswords.selectedIndexes()[0].data()
            with self.db:
                if self.dlg_delete_confirmation() == QMessageBox.Yes:
                    self.db.execute(
                        f"DELETE FROM Password WHERE name='{selected_name}'"
                    )
                    self.update_dashboard_table()
        except IndexError:
            self.dlg_no_row_selected()

    def edit_password(self):
        pass

    def copy_password(self):
        """Inserts the password of the row selected into the clipboard."""
        try:
            selected_row_name = self.ui.tablePasswords.selectedIndexes()[
                0
            ].data()
            with self.db:
                copy_to_cb(
                    self.db.execute(
                        f"SELECT password FROM Password WHERE name='{selected_row_name}'"
                    ).fetchall()[0][0]
                )
        except IndexError:
            self.dlg_no_row_selected()

    # ----- Add New -----
    def update_db(self):
        """
        Inserts the data from the 'Add New' form along with password
        statistics into the database.
        """
        try:
            form_data = [
                self.ui.comboBoxEntryTitle.currentText().replace(" ", ""),
                self.ui.editEntryUrl.text().lower().replace(" ", ""),
                self.ui.editEntryUsername.text().replace(" ", ""),
                self.ui.editEntryPassword.text(),
                self.ui.editEntryPasswordConfirm.text(),
                self.is_password_compromised(self.ui.editEntryPassword.text()),
                self.get_password_strength(self.ui.editEntryPassword.text()),
            ]
            if not (form_data[3] == form_data[4]):
                QMessageBox.warning(
                    self,
                    "Password Manager",
                    "Password confirmation does not match or is empty.",
                )
            elif not (  # Check if each box is full in form.
                sum(1 if i != "" else 0 for i in form_data) == len(form_data)
            ):
                QMessageBox.warning(
                    self,
                    "Password Manager",
                    "All fields are required.",
                )
            elif not is_url_valid(form_data[1]):  # Check if url is valid.
                QMessageBox.critical(
                    self,
                    "Password Manager",
                    "Error: URL is invalid.",
                )
            elif (  # Check if name in entry is found in database.
                not self.is_name_unique(form_data[0])
            ):
                QMessageBox.warning(
                    self,
                    "Password Manager",
                    f"Error: A password for {form_data[0]} already exists.",
                )
            else:
                with self.db:
                    self.db.execute(
                        """
                        INSERT INTO 
                            Password (name, url, username, password, isCompromised, passwordStrength)
                        VALUES
                            (:name, :url, :username, :password, :isCompromised, :passwordStrength)
                        """,
                        {
                            "name": form_data[0],
                            "url": form_data[1],
                            "username": form_data[2],
                            "password": form_data[3],
                            "isCompromised": form_data[5],
                            "passwordStrength": form_data[6],
                        },
                    )
                QMessageBox.information(
                    self,
                    "Password Manager",
                    "Password has been added successfully.",
                )
                self.clear_password_form()
        except urllib.error.URLError:
            self.dlg_no_network()

    def password_toggle(self, checked):
        self.ui.editEntryPassword.setEchoMode(
            QLineEdit.EchoMode.Normal
            if checked
            else QLineEdit.EchoMode.Password
        )
        self.ui.buttonPasswordToggle.setIcon(
            QIcon("icons/eye.svg")
            if checked
            else QIcon("icons/eye-crossed.svg")
        )

    def password_confirm_toggle(self, checked):
        self.ui.editEntryPasswordConfirm.setEchoMode(
            QLineEdit.EchoMode.Normal
            if checked
            else QLineEdit.EchoMode.Password
        )
        self.ui.buttonPasswordToggle2.setIcon(
            QIcon("icons/eye.svg")
            if checked
            else QIcon("icons/eye-crossed.svg")
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
        """Returns a list of the database's data."""
        with self.db:
            return self.db.execute("SELECT * FROM Password").fetchall()

    def is_access_granted(self):
        with self.db:
            try:
                self.db.execute("SELECT count(*) FROM sqlite_master;")
                return True
            except self.db.DatabaseError:
                return False

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
            title_selected = self.ui.comboBoxEntryTitle.currentIndex()
            self.ui.editEntryUrl.setText(url_list[title_selected])
        except IndexError:
            self.ui.editEntryUrl.setText("")

    def clear_password_form(self):
        self.ui.comboBoxEntryTitle.setCurrentIndex(0)
        self.ui.editEntryUsername.clear()
        self.ui.editEntryUrl.clear()
        self.ui.editEntryPassword.clear()
        self.ui.editEntryPasswordConfirm.clear()

    def log_out(self):
        if self.dlg_log_out_confirm() == QMessageBox.Yes:
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

    def is_name_unique(self, name):
        with self.db:
            try:
                return not name in [
                    i[0]
                    for i in self.db.execute(
                        "SELECT name FROM Password"
                    ).fetchall()
                ]
            except sqlcipher.DatabaseError:
                return True
