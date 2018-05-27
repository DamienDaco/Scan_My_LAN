import sys
from app.model import *
from ui.Scan_My_LAN import *
from app.view import *
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow


if __name__ == "__main__":

    app = QApplication(sys.argv)

    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    model = Model()
    sys.exit(app.exec_())