# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.6.1
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
from PySide6.QtWidgets import (QApplication, QGraphicsView, QGridLayout, QGroupBox,
    QHBoxLayout, QLabel, QLineEdit, QMainWindow,
    QMenuBar, QPushButton, QSizePolicy, QStatusBar,
    QTextEdit, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")
        self.verticalLayout = QVBoxLayout(self.widget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.title = QLabel(self.widget)
        self.title.setObjectName(u"title")
        self.title.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.title)

        self.widget_2 = QWidget(self.widget)
        self.widget_2.setObjectName(u"widget_2")
        self.horizontalLayout_2 = QHBoxLayout(self.widget_2)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.groupBox = QGroupBox(self.widget_2)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout_2 = QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setSpacing(4)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(5, -1, 5, 5)
        self.widget_3 = QWidget(self.groupBox)
        self.widget_3.setObjectName(u"widget_3")
        self.widget_3.setMinimumSize(QSize(0, 170))
        self.gridLayout = QGridLayout(self.widget_3)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_3 = QLabel(self.widget_3)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)

        self.A_point = QLineEdit(self.widget_3)
        self.A_point.setObjectName(u"A_point")

        self.gridLayout.addWidget(self.A_point, 0, 1, 1, 1)

        self.label = QLabel(self.widget_3)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.line_edit = QLineEdit(self.widget_3)
        self.line_edit.setObjectName(u"line_edit")

        self.gridLayout.addWidget(self.line_edit, 3, 1, 1, 1)

        self.label_4 = QLabel(self.widget_3)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 1)

        self.label_2 = QLabel(self.widget_3)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)

        self.B_point = QLineEdit(self.widget_3)
        self.B_point.setObjectName(u"B_point")

        self.gridLayout.addWidget(self.B_point, 1, 1, 1, 1)

        self.C_point = QLineEdit(self.widget_3)
        self.C_point.setObjectName(u"C_point")

        self.gridLayout.addWidget(self.C_point, 2, 1, 1, 1)


        self.verticalLayout_2.addWidget(self.widget_3)

        self.widget_5 = QWidget(self.groupBox)
        self.widget_5.setObjectName(u"widget_5")
        self.widget_5.setMaximumSize(QSize(16777215, 40))
        self.horizontalLayout_3 = QHBoxLayout(self.widget_5)
        self.horizontalLayout_3.setSpacing(1)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(1, 1, 1, 1)
        self.pushButton = QPushButton(self.widget_5)
        self.pushButton.setObjectName(u"pushButton")

        self.horizontalLayout_3.addWidget(self.pushButton)

        self.pushButton_2 = QPushButton(self.widget_5)
        self.pushButton_2.setObjectName(u"pushButton_2")

        self.horizontalLayout_3.addWidget(self.pushButton_2)

        self.pushButton_3 = QPushButton(self.widget_5)
        self.pushButton_3.setObjectName(u"pushButton_3")

        self.horizontalLayout_3.addWidget(self.pushButton_3)


        self.verticalLayout_2.addWidget(self.widget_5)

        self.widget_4 = QWidget(self.groupBox)
        self.widget_4.setObjectName(u"widget_4")
        self.verticalLayout_3 = QVBoxLayout(self.widget_4)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.textEdit = QTextEdit(self.widget_4)
        self.textEdit.setObjectName(u"textEdit")
        self.textEdit.setReadOnly(True)

        self.verticalLayout_3.addWidget(self.textEdit)

        self.widget_6 = QWidget(self.widget_4)
        self.widget_6.setObjectName(u"widget_6")
        self.horizontalLayout_4 = QHBoxLayout(self.widget_6)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.pushButton_4 = QPushButton(self.widget_6)
        self.pushButton_4.setObjectName(u"pushButton_4")

        self.horizontalLayout_4.addWidget(self.pushButton_4)

        self.pushButton_5 = QPushButton(self.widget_6)
        self.pushButton_5.setObjectName(u"pushButton_5")

        self.horizontalLayout_4.addWidget(self.pushButton_5)


        self.verticalLayout_3.addWidget(self.widget_6)


        self.verticalLayout_2.addWidget(self.widget_4)


        self.horizontalLayout_2.addWidget(self.groupBox)

        self.graphicsView = QGraphicsView(self.widget_2)
        self.graphicsView.setObjectName(u"graphicsView")

        self.horizontalLayout_2.addWidget(self.graphicsView)


        self.verticalLayout.addWidget(self.widget_2)


        self.horizontalLayout.addWidget(self.widget)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.title.setText(QCoreApplication.translate("MainWindow", u"\u4e8c\u7ef4\u56fe\u5f62\u5750\u6807\u53d8\u6362\u5206\u89e3", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"\u83dc\u5355", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"C\u70b9\u5750\u6807", None))
        self.A_point.setInputMask("")
        self.A_point.setText("")
        self.A_point.setPlaceholderText(QCoreApplication.translate("MainWindow", u"(-1.25,4.5)", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"A\u70b9\u5750\u6807", None))
        self.line_edit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"4x+5y-7=0", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"\u76f4\u7ebf\u8868\u8fbe\u5f0f", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"B\u70b9\u5750\u6807", None))
        self.B_point.setPlaceholderText(QCoreApplication.translate("MainWindow", u"(2.5,1)", None))
        self.C_point.setPlaceholderText(QCoreApplication.translate("MainWindow", u"(-3,-3)", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"\u751f\u6210\u968f\u673a\u503c", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"\u786e\u5b9a", None))
        self.pushButton_3.setText(QCoreApplication.translate("MainWindow", u"\u53d6\u6d88", None))
        self.pushButton_4.setText(QCoreApplication.translate("MainWindow", u"\u5bfc\u51fa\u8ba1\u7b97\u7ed3\u679c", None))
        self.pushButton_5.setText(QCoreApplication.translate("MainWindow", u"\u5e2e\u52a9", None))
    # retranslateUi

