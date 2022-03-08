# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'log_in.ui'
##
## Created by: Qt User Interface Compiler version 6.2.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLabel,
    QLineEdit, QMainWindow, QPushButton, QSizePolicy,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(330, 380)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.frame = QFrame(self.centralwidget)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.NoFrame)
        self.frame.setFrameShadow(QFrame.Raised)
        self.buttonSubmit = QPushButton(self.frame)
        self.buttonSubmit.setObjectName(u"buttonSubmit")
        self.buttonSubmit.setGeometry(QRect(30, 300, 251, 27))
        self.buttonSubmit.setMinimumSize(QSize(0, 27))
        font = QFont()
        font.setFamilies([u"Roboto"])
        font.setPointSize(9)
        self.buttonSubmit.setFont(font)
        self.buttonSubmit.setCursor(QCursor(Qt.PointingHandCursor))
        self.buttonSubmit.setFlat(False)
        self.layoutWidget = QWidget(self.frame)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(29, 30, 251, 67))
        self.verticalLayout = QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.labelHeading = QLabel(self.layoutWidget)
        self.labelHeading.setObjectName(u"labelHeading")
        font1 = QFont()
        font1.setFamilies([u"Roboto Medium"])
        font1.setPointSize(14)
        font1.setBold(False)
        self.labelHeading.setFont(font1)
        self.labelHeading.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.verticalLayout.addWidget(self.labelHeading)

        self.labelSubHeading = QLabel(self.layoutWidget)
        self.labelSubHeading.setObjectName(u"labelSubHeading")
        font2 = QFont()
        font2.setFamilies([u"Roboto Light"])
        font2.setPointSize(8)
        font2.setBold(False)
        font2.setItalic(False)
        font2.setUnderline(False)
        self.labelSubHeading.setFont(font2)
        self.labelSubHeading.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.labelSubHeading.setWordWrap(True)
        self.labelSubHeading.setMargin(2)

        self.verticalLayout.addWidget(self.labelSubHeading)

        self.layoutWidget1 = QWidget(self.frame)
        self.layoutWidget1.setObjectName(u"layoutWidget1")
        self.layoutWidget1.setGeometry(QRect(30, 120, 251, 77))
        self.verticalLayout_3 = QVBoxLayout(self.layoutWidget1)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.labelPassword1 = QLabel(self.layoutWidget1)
        self.labelPassword1.setObjectName(u"labelPassword1")
        font3 = QFont()
        font3.setFamilies([u"Roboto"])
        font3.setPointSize(9)
        font3.setUnderline(False)
        self.labelPassword1.setFont(font3)

        self.verticalLayout_2.addWidget(self.labelPassword1)

        self.labelPassword1Sub = QLabel(self.layoutWidget1)
        self.labelPassword1Sub.setObjectName(u"labelPassword1Sub")
        font4 = QFont()
        font4.setFamilies([u"Roboto Light"])
        font4.setPointSize(8)
        font4.setItalic(True)
        font4.setUnderline(False)
        self.labelPassword1Sub.setFont(font4)

        self.verticalLayout_2.addWidget(self.labelPassword1Sub)


        self.verticalLayout_3.addLayout(self.verticalLayout_2)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.editPassword1 = QLineEdit(self.layoutWidget1)
        self.editPassword1.setObjectName(u"editPassword1")
        self.editPassword1.setMinimumSize(QSize(0, 25))
        font5 = QFont()
        font5.setFamilies([u"Roboto"])
        font5.setPointSize(8)
        self.editPassword1.setFont(font5)
        self.editPassword1.setEchoMode(QLineEdit.Password)
        self.editPassword1.setClearButtonEnabled(True)

        self.horizontalLayout_2.addWidget(self.editPassword1)

        self.buttonPasswordToggle1 = QPushButton(self.layoutWidget1)
        self.buttonPasswordToggle1.setObjectName(u"buttonPasswordToggle1")
        self.buttonPasswordToggle1.setMinimumSize(QSize(27, 27))
        self.buttonPasswordToggle1.setFont(font5)
        self.buttonPasswordToggle1.setCursor(QCursor(Qt.PointingHandCursor))
        icon = QIcon()
        icon.addFile(u"icons/eye-crossed.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.buttonPasswordToggle1.setIcon(icon)
        self.buttonPasswordToggle1.setIconSize(QSize(14, 14))

        self.horizontalLayout_2.addWidget(self.buttonPasswordToggle1)


        self.verticalLayout_3.addLayout(self.horizontalLayout_2)

        self.layoutWidget2 = QWidget(self.frame)
        self.layoutWidget2.setObjectName(u"layoutWidget2")
        self.layoutWidget2.setGeometry(QRect(30, 210, 251, 54))
        self.verticalLayout_4 = QVBoxLayout(self.layoutWidget2)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.labelPassword2 = QLabel(self.layoutWidget2)
        self.labelPassword2.setObjectName(u"labelPassword2")
        self.labelPassword2.setFont(font)

        self.verticalLayout_4.addWidget(self.labelPassword2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.editPassword2 = QLineEdit(self.layoutWidget2)
        self.editPassword2.setObjectName(u"editPassword2")
        self.editPassword2.setMinimumSize(QSize(0, 25))
        self.editPassword2.setFont(font5)
        self.editPassword2.setEchoMode(QLineEdit.Password)
        self.editPassword2.setClearButtonEnabled(True)

        self.horizontalLayout_3.addWidget(self.editPassword2)

        self.buttonPasswordToggle2 = QPushButton(self.layoutWidget2)
        self.buttonPasswordToggle2.setObjectName(u"buttonPasswordToggle2")
        self.buttonPasswordToggle2.setMinimumSize(QSize(27, 27))
        self.buttonPasswordToggle2.setFont(font5)
        self.buttonPasswordToggle2.setCursor(QCursor(Qt.PointingHandCursor))
        self.buttonPasswordToggle2.setIcon(icon)
        self.buttonPasswordToggle2.setIconSize(QSize(14, 14))

        self.horizontalLayout_3.addWidget(self.buttonPasswordToggle2)


        self.verticalLayout_4.addLayout(self.horizontalLayout_3)


        self.horizontalLayout.addWidget(self.frame)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.buttonSubmit.setDefault(False)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.buttonSubmit.setText(QCoreApplication.translate("MainWindow", u"Create", None))
        self.labelHeading.setText(QCoreApplication.translate("MainWindow", u"Create a Master Password", None))
        self.labelSubHeading.setText(QCoreApplication.translate("MainWindow", u"This is the password you must remember in order to access your password vault. ", None))
        self.labelPassword1.setText(QCoreApplication.translate("MainWindow", u"Master Password", None))
        self.labelPassword1Sub.setText(QCoreApplication.translate("MainWindow", u"Must have 8 characters or more", None))
        self.editPassword1.setText("")
        self.editPassword1.setPlaceholderText("")
        self.labelPassword2.setText(QCoreApplication.translate("MainWindow", u"Confirm Master Password", None))
        self.editPassword2.setText("")
        self.editPassword2.setPlaceholderText("")
    # retranslateUi

Error: log_in.ui: Warning: The name 'layoutWidget' (QWidget) is already in use, defaulting to 'layoutWidget1'.
log_in.ui: Warning: The name 'layoutWidget' (QWidget) is already in use, defaulting to 'layoutWidget2'.

while executing '/home/emuel/.local/lib/python3.8/site-packages/PySide6/Qt/libexec/uic -g python log_in.ui'
