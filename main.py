from os import system
from qdarktheme import load_stylesheet
from sys import exit as sys_exit

from PySide6.QtWidgets import QApplication, QStackedLayout

system("pyside6-uic main_window.ui > ui_main_window.py")
from window_log_in import MainWindow as LogInWindow

system("pyside6-uic log_in.ui > ui_log_in.py")
from window_main import MainWindow


def main():
    app = QApplication([])
    app.setStyleSheet(load_stylesheet())

    layout = QStackedLayout()

    log_in_window = LogInWindow()
    layout.addWidget(log_in_window)

    main_window = MainWindow()
    layout.addWidget(main_window)

    layout.setCurrentWidget(log_in_window)

    log_in_window.logged_in.connect(
        lambda w=main_window: layout.setCurrentWidget(w)
    )
    sys_exit(app.exec())


if __name__ == "__main__":
    main()
