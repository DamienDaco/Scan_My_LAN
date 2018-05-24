# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Scan_My_LAN.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(515, 341)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.table_view = QtWidgets.QTableView(self.centralwidget)
        self.table_view.setObjectName("table_view")
        self.gridLayout.addWidget(self.table_view, 1, 0, 1, 1)
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.frame)
        self.gridLayout_2.setObjectName("gridLayout_2")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 0, 2, 1, 1)
        self.debug_button = QtWidgets.QPushButton(self.frame)
        self.debug_button.setObjectName("debug_button")
        self.gridLayout_2.addWidget(self.debug_button, 0, 1, 1, 1)
        self.start_button = QtWidgets.QPushButton(self.frame)
        self.start_button.setObjectName("start_button")
        self.gridLayout_2.addWidget(self.start_button, 0, 0, 1, 1)
        self.interface_box = QtWidgets.QComboBox(self.frame)
        self.interface_box.setObjectName("interface_box")
        self.gridLayout_2.addWidget(self.interface_box, 0, 3, 1, 1)
        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 515, 30))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.action_start = QtWidgets.QAction(MainWindow)
        self.action_start.setObjectName("action_start")
        self.action_debug = QtWidgets.QAction(MainWindow)
        self.action_debug.setObjectName("action_debug")
        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.menuFile.addAction(self.actionSave)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Scan My LAN"))
        self.debug_button.setText(_translate("MainWindow", "Debug"))
        self.start_button.setText(_translate("MainWindow", "Start"))
        self.menuFile.setTitle(_translate("MainWindow", "Fi&le"))
        self.action_start.setText(_translate("MainWindow", "Start"))
        self.action_start.setToolTip(_translate("MainWindow", "Start"))
        self.action_debug.setText(_translate("MainWindow", "Debug"))
        self.action_debug.setToolTip(_translate("MainWindow", "Various debugging stuff"))
        self.actionSave.setText(_translate("MainWindow", "&Save"))

