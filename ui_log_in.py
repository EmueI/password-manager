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
from PySide6.QtWidgets import (QApplication, QFrame, QGroupBox, QHBoxLayout,
    QLabel, QLineEdit, QMainWindow, QPushButton,
    QSizePolicy, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(342, 370)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.buttonSubmit = QPushButton(self.centralwidget)
        self.buttonSubmit.setObjectName(u"buttonSubmit")
        self.buttonSubmit.setGeometry(QRect(40, 310, 260, 27))
        self.buttonSubmit.setMinimumSize(QSize(0, 27))
        font = QFont()
        font.setFamilies([u"Roboto"])
        font.setPointSize(8)
        self.buttonSubmit.setFont(font)
        self.buttonSubmit.setCursor(QCursor(Qt.PointingHandCursor))
        self.buttonSubmit.setFlat(False)
        self.groupBoxMain = QGroupBox(self.centralwidget)
        self.groupBoxMain.setObjectName(u"groupBoxMain")
        self.groupBoxMain.setGeometry(QRect(40, 130, 261, 81))
        font1 = QFont()
        font1.setFamilies([u"Roboto"])
        self.groupBoxMain.setFont(font1)
        self.verticalLayout = QVBoxLayout(self.groupBoxMain)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(self.groupBoxMain)
        self.label.setObjectName(u"label")
        font2 = QFont()
        font2.setFamilies([u"Roboto"])
        font2.setPointSize(8)
        font2.setItalic(True)
        self.label.setFont(font2)

        self.verticalLayout.addWidget(self.label)

        self.frame = QFrame(self.groupBoxMain)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.NoFrame)
        self.horizontalLayout_2 = QHBoxLayout(self.frame)
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.editPasswordMain = QLineEdit(self.frame)
        self.editPasswordMain.setObjectName(u"editPasswordMain")
        self.editPasswordMain.setMinimumSize(QSize(0, 25))
        font3 = QFont()
        font3.setFamilies([u"Roboto"])
        font3.setPointSize(10)
        self.editPasswordMain.setFont(font3)
        self.editPasswordMain.setEchoMode(QLineEdit.Password)
        self.editPasswordMain.setClearButtonEnabled(True)

        self.horizontalLayout_2.addWidget(self.editPasswordMain)

        self.buttonPasswordToggle1 = QPushButton(self.frame)
        self.buttonPasswordToggle1.setObjectName(u"buttonPasswordToggle1")
        self.buttonPasswordToggle1.setMinimumSize(QSize(27, 27))
        self.buttonPasswordToggle1.setFont(font)
        self.buttonPasswordToggle1.setCursor(QCursor(Qt.PointingHandCursor))
        icon = QIcon()
        icon.addFile(u"icons/eye-crossed.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.buttonPasswordToggle1.setIcon(icon)
        self.buttonPasswordToggle1.setIconSize(QSize(14, 14))

        self.horizontalLayout_2.addWidget(self.buttonPasswordToggle1)


        self.verticalLayout.addWidget(self.frame)

        self.groupBoxConfirm = QGroupBox(self.centralwidget)
        self.groupBoxConfirm.setObjectName(u"groupBoxConfirm")
        self.groupBoxConfirm.setGeometry(QRect(40, 220, 260, 60))
        self.groupBoxConfirm.setFont(font1)
        self.horizontalLayout = QHBoxLayout(self.groupBoxConfirm)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.editPasswordConfirm = QLineEdit(self.groupBoxConfirm)
        self.editPasswordConfirm.setObjectName(u"editPasswordConfirm")
        self.editPasswordConfirm.setMinimumSize(QSize(0, 25))
        self.editPasswordConfirm.setFont(font3)
        self.editPasswordConfirm.setEchoMode(QLineEdit.Password)
        self.editPasswordConfirm.setClearButtonEnabled(True)

        self.horizontalLayout.addWidget(self.editPasswordConfirm)

        self.buttonPasswordToggle2 = QPushButton(self.groupBoxConfirm)
        self.buttonPasswordToggle2.setObjectName(u"buttonPasswordToggle2")
        self.buttonPasswordToggle2.setMinimumSize(QSize(27, 27))
        self.buttonPasswordToggle2.setFont(font)
        self.buttonPasswordToggle2.setCursor(QCursor(Qt.PointingHandCursor))
        self.buttonPasswordToggle2.setIcon(icon)
        self.buttonPasswordToggle2.setIconSize(QSize(14, 14))

        self.horizontalLayout.addWidget(self.buttonPasswordToggle2)

        self.labelSubHeading = QLabel(self.centralwidget)
        self.labelSubHeading.setObjectName(u"labelSubHeading")
        self.labelSubHeading.setGeometry(QRect(40, 70, 261, 26))
        self.labelSubHeading.setFont(font)
        self.labelSubHeading.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.labelSubHeading.setWordWrap(True)
        self.labelSubHeading.setTextInteractionFlags(Qt.NoTextInteraction)
        self.labelHeading = QLabel(self.centralwidget)
        self.labelHeading.setObjectName(u"labelHeading")
        self.labelHeading.setGeometry(QRect(40, 40, 261, 23))
        font4 = QFont()
        font4.setFamilies([u"Roboto Medium"])
        font4.setPointSize(14)
        self.labelHeading.setFont(font4)
        self.labelHeading.setTextInteractionFlags(Qt.NoTextInteraction)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.buttonSubmit.setDefault(False)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.buttonSubmit.setText(QCoreApplication.translate("MainWindow", u"Create", None))
        self.groupBoxMain.setTitle(QCoreApplication.translate("MainWindow", u"Master password", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Use at least 8 characters", None))
        self.editPasswordMain.setText("")
        self.editPasswordMain.setPlaceholderText("")
        self.groupBoxConfirm.setTitle(QCoreApplication.translate("MainWindow", u"Confirm master password", None))
        self.editPasswordConfirm.setText("")
        self.editPasswordConfirm.setPlaceholderText("")
        self.labelSubHeading.setText(QCoreApplication.translate("MainWindow", u"This is the password you must remember in order to access your password vault. ", None))
        self.labelHeading.setText(QCoreApplication.translate("MainWindow", u"Create your Master Password", None))
    # retranslateUi

