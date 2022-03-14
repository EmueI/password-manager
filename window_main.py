from keyring import get_password as keyring_get_password
from os.path import exists
from password_strength import PasswordStats
from pwnedpasswords import check as check_pwned
from pysqlitecipher.sqlitewrapper import SqliteCipher
from pyperclip import copy as copy_to_cb
from secrets import choice as secrets_choice
from string import ascii_uppercase, ascii_lowercase, digits
from sys import exit as exit_window
from validators import url as is_url_valid

from PySide6.QtCore import Qt, QSortFilterProxyModel, QModelIndex
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
        self.ui.editEntryUrl.returnPressed.connect(self.update_db)
        self.ui.editEntryUsername.returnPressed.connect(self.update_db)
        self.ui.editEntryPassword.returnPressed.connect(self.update_db)
        self.ui.buttonPasswordToggle.clicked.connect(self.password_toggle)
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
            self.ui.comboBoxEntryTitle.currentText(),
            self.ui.editEntryUrl.text().lower(),
            self.ui.editEntryUsername.text(),
            self.ui.editEntryPassword.text(),
            self.is_password_compromised(self.ui.editEntryPassword.text()),
            self.get_password_strength(self.ui.editEntryPassword.text()),
        ]

        # Check if all fields in the form are filled.
        if sum(1 if i != "" else 0 for i in form_data) != len(form_data):
            self.dlg_form_not_filled()
        # Check if URL is valid.
        elif self.ui.editEntryUrl.text().replace(
            " ", ""
        ) != "" and not is_url_valid(self.ui.editEntryUrl.text().lower()):
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
            self.ui.editEntryPassword.setEchoMode(QLineEdit.EchoMode.Normal)
            self.ui.buttonPasswordToggle.setIcon(QIcon("icons/eye.svg"))
        else:
            self.ui.editEntryPassword.setEchoMode(QLineEdit.EchoMode.Password)
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
            title_selected = self.ui.comboBoxEntryTitle.currentIndex()
            self.ui.editEntryUrl.setText(url_list[title_selected])
        except IndexError:
            self.ui.editEntryUrl.setText("")

    def clear_password_form(self):
        self.ui.comboBoxEntryTitle.setCurrentIndex(0)
        self.ui.editEntryUsername.clear()
        self.ui.editEntryUrl.clear()
        self.ui.editEntryPassword.clear()

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
