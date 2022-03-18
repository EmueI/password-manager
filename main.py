from qdarktheme import load_stylesheet
from qdarktheme import load_stylesheet
from sys import exit as sys_exit
from os import system
from pysqlcipher3 import dbapi2 as sqlcipher

from PySide6.QtWidgets import QApplication, QStackedLayout

system("pyside6-uic log_in.ui > ui_log_in.py")
from window_log_in import LogInWindow

system("pyside6-uic main_window.ui > ui_main_window.py")
from window_main import MainWindow


def main():
    app = QApplication([])
    app.setStyleSheet(load_stylesheet("dark", "rounded"))

    db = sqlcipher.connect("passwordManager.db")

    log_in_window = LogInWindow(db)
    main_window = MainWindow(db, log_in_window.master_password_input)

    layout = QStackedLayout()
    layout.addWidget(log_in_window)
    layout.addWidget(main_window)
    layout.setCurrentWidget(log_in_window)

    log_in_window.logged_in.connect(
        lambda w=main_window: layout.setCurrentWidget(w)
    )
    sys_exit(app.exec())


if __name__ == "__main__":
    main()
