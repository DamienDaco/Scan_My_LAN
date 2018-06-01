from app.multithreading import *


class Model:

    def __init__(self):
        super().__init__()

        self.default_interface = get_default_interface()
        self.selected_interface = self.default_interface
        self.interface_list = get_interfaces()

        self.get_selected_interface_info()

    def get_selected_interface_info(self):
        self.my_mac = get_mac(self.selected_interface)
        self.my_ip = get_host_ip(self.selected_interface)
        self.my_mask = get_host_mask(self.selected_interface)

        self.hex_mac = hex_mac(self.my_mac)
        self.decimal_ip = decimal_ip(self.my_ip)



