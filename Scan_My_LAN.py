from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from app.network_functions import *

from ui.Scan_My_LAN import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super().__init__()

        self.setupUi(self)

        self.default_interface = get_default_interface()
        self.my_mac = get_mac(self.default_interface)
        self.my_ip = get_host_ip(self.default_interface)

        print("Your default interface is {}, your IP is {} and your MAC is {}".format(self.default_interface, self.my_ip, self.my_mac))


if __name__ == "__main__":

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())