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
        MainWindow.resize(415, 354)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.table_view = QtWidgets.QTableView(self.centralwidget)
        self.table_view.setObjectName("table_view")
        self.gridLayout.addWidget(self.table_view, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 415, 30))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.action_start = QtWidgets.QAction(MainWindow)
        self.action_start.setObjectName("action_start")
        self.action_debug = QtWidgets.QAction(MainWindow)
        self.action_debug.setObjectName("action_debug")
        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.menuFile.addAction(self.actionSave)
        self.menubar.addAction(self.menuFile.menuAction())
        self.toolBar.addAction(self.action_start)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.action_debug)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Scan My LAN"))
        self.menuFile.setTitle(_translate("MainWindow", "Fi&le"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.action_start.setText(_translate("MainWindow", "Start"))
        self.action_start.setToolTip(_translate("MainWindow", "Start"))
        self.action_debug.setText(_translate("MainWindow", "Debug"))
        self.action_debug.setToolTip(_translate("MainWindow", "Various debugging stuff"))
        self.actionSave.setText(_translate("MainWindow", "Save"))

