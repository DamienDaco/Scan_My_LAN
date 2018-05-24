from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from app.logic import *

from ui.Scan_My_LAN import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super().__init__()

        self.setupUi(self)

        self.logic = Logic()

        self.interface_box.addItems(self.logic.interface_list)
        self.interface_box.setCurrentText(self.logic.default_interface)
        print("Your default interface is {}, your IP is {} and your MAC is {}".format(self.logic.default_interface, self.logic.my_ip, self.logic.my_mac))


if __name__ == "__main__":

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())