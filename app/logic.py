from app.network_functions import *
from app.mainwindow import MainWindow


class Logic:

    def __init__(self):
        super().__init__()

        self.default_interface = get_default_interface()
        self.my_mac = get_mac(self.default_interface)
        self.my_ip = get_host_ip(self.default_interface)
        self.my_mask = get_host_mask(self.default_interface)

        self.interface_list = get_interfaces()

        self.main_window = MainWindow()
        self.main_window.show()

        self.main_window.interface_box.addItems(self.interface_list)
        self.main_window.interface_box.setCurrentText(self.default_interface)

        print("Your default interface is {}, your IP is {}, your mask is {} and your MAC is {}".format(self.default_interface, self.my_ip, self.my_mask, self.my_mac))