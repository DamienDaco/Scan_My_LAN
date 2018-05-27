# from PyQt5.QtGui import *
# from app.model import *
from app.network_functions import *
import struct

class Controller:

    def __init__(self, view, model):

        self.model = model
        self.view = view
        self.view.set_controller(self)

        self.view.start()

    def calc_range(self):

        calc_range(self.model.my_ip, self.model.my_mask)

    def send_arp_queries(self):

        self.first_ip, self.last_ip = calc_range(self.model.my_ip, self.model.my_mask)

        for i in range(self.first_ip, self.last_ip + 1):

            send_data(self.model.default_interface, build_arp_query(self.model.hex_mac, self.model.decimal_ip, i))


