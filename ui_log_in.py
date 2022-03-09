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
        self.buttonSubmit = QPushButton(self.centralwidget)
        self.buttonSubmit.setObjectName(u"buttonSubmit")
        self.buttonSubmit.setGeometry(QRect(40, 300, 251, 27))
        self.buttonSubmit.setMinimumSize(QSize(0, 27))
        font = QFont()
        font.setFamilies([u"Roboto"])
        font.setPointSize(9)
        self.buttonSubmit.setFont(font)
        self.buttonSubmit.setCursor(QCursor(Qt.PointingHandCursor))
        self.buttonSubmit.setFlat(False)
        self.frameMainPwd2 = QFrame(self.centralwidget)
        self.frameMainPwd2.setObjectName(u"frameMainPwd2")
        self.frameMainPwd2.setGeometry(QRect(40, 210, 251, 61))
        self.frameMainPwd2.setFrameShape(QFrame.NoFrame)
        self.frameMainPwd2.setFrameShadow(QFrame.Raised)
        self.verticalLayout = QVBoxLayout(self.frameMainPwd2)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.labelPassword2 = QLabel(self.frameMainPwd2)
        self.labelPassword2.setObjectName(u"labelPassword2")
        self.labelPassword2.setFont(font)

        self.verticalLayout.addWidget(self.labelPassword2)

        self.framePwdEntry2 = QFrame(self.frameMainPwd2)
        self.framePwdEntry2.setObjectName(u"framePwdEntry2")
        self.framePwdEntry2.setFrameShape(QFrame.NoFrame)
        self.framePwdEntry2.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(self.framePwdEntry2)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.editPassword2 = QLineEdit(self.framePwdEntry2)
        self.editPassword2.setObjectName(u"editPassword2")
        self.editPassword2.setMinimumSize(QSize(0, 25))
        font1 = QFont()
        font1.setFamilies([u"Roboto"])
        font1.setPointSize(8)
        self.editPassword2.setFont(font1)
        self.editPassword2.setEchoMode(QLineEdit.Password)
        self.editPassword2.setClearButtonEnabled(True)

        self.horizontalLayout.addWidget(self.editPassword2)

        self.buttonPasswordToggle2 = QPushButton(self.framePwdEntry2)
        self.buttonPasswordToggle2.setObjectName(u"buttonPasswordToggle2")
        self.buttonPasswordToggle2.setMinimumSize(QSize(27, 27))
        self.buttonPasswordToggle2.setFont(font1)
        self.buttonPasswordToggle2.setCursor(QCursor(Qt.PointingHandCursor))
        icon = QIcon()
        icon.addFile(u"icons/eye-crossed.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.buttonPasswordToggle2.setIcon(icon)
        self.buttonPasswordToggle2.setIconSize(QSize(14, 14))

        self.horizontalLayout.addWidget(self.buttonPasswordToggle2)


        self.verticalLayout.addWidget(self.framePwdEntry2)

        self.frame = QFrame(self.centralwidget)
        self.frame.setObjectName(u"frame")
        self.frame.setGeometry(QRect(40, 30, 251, 76))
        self.frame.setFrameShape(QFrame.NoFrame)
        self.frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.frame)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.labelHeading = QLabel(self.frame)
        self.labelHeading.setObjectName(u"labelHeading")
        font2 = QFont()
        font2.setFamilies([u"Roboto Medium"])
        font2.setPointSize(14)
        self.labelHeading.setFont(font2)

        self.verticalLayout_3.addWidget(self.labelHeading)

        self.labelSubHeading = QLabel(self.frame)
        self.labelSubHeading.setObjectName(u"labelSubHeading")
        font3 = QFont()
        font3.setFamilies([u"Roboto Light"])
        font3.setPointSize(8)
        self.labelSubHeading.setFont(font3)
        self.labelSubHeading.setWordWrap(True)

        self.verticalLayout_3.addWidget(self.labelSubHeading)

        self.frameMainPwd1 = QFrame(self.centralwidget)
        self.frameMainPwd1.setObjectName(u"frameMainPwd1")
        self.frameMainPwd1.setGeometry(QRect(40, 130, 251, 82))
        self.frameMainPwd1.setFrameShape(QFrame.NoFrame)
        self.frameMainPwd1.setFrameShadow(QFrame.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.frameMainPwd1)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.frame_4 = QFrame(self.frameMainPwd1)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setFrameShape(QFrame.NoFrame)
        self.frame_4.setFrameShadow(QFrame.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.frame_4)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.labelPassword1 = QLabel(self.frame_4)
        self.labelPassword1.setObjectName(u"labelPassword1")
        font4 = QFont()
        font4.setFamilies([u"Roboto"])
        font4.setPointSize(9)
        font4.setUnderline(False)
        self.labelPassword1.setFont(font4)

        self.verticalLayout_2.addWidget(self.labelPassword1)

        self.labelPassword1Sub = QLabel(self.frame_4)
        self.labelPassword1Sub.setObjectName(u"labelPassword1Sub")
        font5 = QFont()
        font5.setFamilies([u"Roboto Light"])
        font5.setPointSize(8)
        font5.setItalic(True)
        font5.setUnderline(False)
        self.labelPassword1Sub.setFont(font5)

        self.verticalLayout_2.addWidget(self.labelPassword1Sub)


        self.verticalLayout_4.addWidget(self.frame_4)

        self.framePwdEntry1 = QFrame(self.frameMainPwd1)
        self.framePwdEntry1.setObjectName(u"framePwdEntry1")
        self.framePwdEntry1.setFrameShape(QFrame.NoFrame)
        self.framePwdEntry1.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.framePwdEntry1)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.editPassword1 = QLineEdit(self.framePwdEntry1)
        self.editPassword1.setObjectName(u"editPassword1")
        self.editPassword1.setMinimumSize(QSize(0, 25))
        self.editPassword1.setFont(font1)
        self.editPassword1.setEchoMode(QLineEdit.Password)
        self.editPassword1.setClearButtonEnabled(True)

        self.horizontalLayout_2.addWidget(self.editPassword1)

        self.buttonPasswordToggle1 = QPushButton(self.framePwdEntry1)
        self.buttonPasswordToggle1.setObjectName(u"buttonPasswordToggle1")
        self.buttonPasswordToggle1.setMinimumSize(QSize(27, 27))
        self.buttonPasswordToggle1.setFont(font1)
        self.buttonPasswordToggle1.setCursor(QCursor(Qt.PointingHandCursor))
        self.buttonPasswordToggle1.setIcon(icon)
        self.buttonPasswordToggle1.setIconSize(QSize(14, 14))

        self.horizontalLayout_2.addWidget(self.buttonPasswordToggle1)


        self.verticalLayout_4.addWidget(self.framePwdEntry1)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.buttonSubmit.setDefault(False)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.buttonSubmit.setText(QCoreApplication.translate("MainWindow", u"Create", None))
        self.labelPassword2.setText(QCoreApplication.translate("MainWindow", u"Confirm Master Password", None))
        self.editPassword2.setText("")
        self.editPassword2.setPlaceholderText("")
        self.labelHeading.setText(QCoreApplication.translate("MainWindow", u"Create a Master Password", None))
        self.labelSubHeading.setText(QCoreApplication.translate("MainWindow", u"This is the password you must remember in order to access your password vault. ", None))
        self.labelPassword1.setText(QCoreApplication.translate("MainWindow", u"Master Password", None))
        self.labelPassword1Sub.setText(QCoreApplication.translate("MainWindow", u"Must have 8 characters or more", None))
        self.editPassword1.setText("")
        self.editPassword1.setPlaceholderText("")
    # retranslateUi

