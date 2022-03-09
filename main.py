from qdarktheme import load_stylesheet
from PySide6.QtWidgets import QApplication, QStackedLayout
from functools import partial
from sys import exit
from os import system

system(
    "pyside6-uic main_window.ui > ui_main_window.py && pyside6-uic log_in.ui > ui_log_in.py"
)
from window_log_in import MainWindow as LogInWindow
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
    exit(app.exec())


if __name__ == "__main__":
    main()
