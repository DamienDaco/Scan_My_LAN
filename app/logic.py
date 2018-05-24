from app.network_functions import *


class Logic:

    def __init__(self):
        super().__init__()

        self.default_interface = get_default_interface()
        self.my_mac = get_mac(self.default_interface)
        self.my_ip = get_host_ip(self.default_interface)

        self.interface_list = get_interfaces()