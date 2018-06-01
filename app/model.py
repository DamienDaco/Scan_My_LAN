from app.network_functions import *
from app.multithreading import *
# from app.view import MainWindow


class Model:

    def __init__(self):
        super().__init__()

        self.default_interface = get_default_interface()
        self.selected_interface = self.default_interface
        self.my_mac = get_mac(self.default_interface)
        self.my_ip = get_host_ip(self.default_interface)
        self.my_mask = get_host_mask(self.default_interface)

        self.hex_mac = hex_mac(self.my_mac)
        self.decimal_ip = decimal_ip(self.my_ip)

        self.interface_list = get_interfaces()

        # self.main_window.interface_box.addItems(self.interface_list)
        # self.main_window.interface_box.setCurrentText(self.default_interface)

        print("Your default interface is {}, your IP is {}, your mask is {} and your MAC is {}".format(
              self.default_interface, self.my_ip, self.my_mask, self.my_mac))



