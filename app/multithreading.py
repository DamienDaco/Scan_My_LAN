from PyQt5.QtCore import *
from app.network_functions import *


class ArpQueryWorker(QObject):
    str_signal = pyqtSignal(str)
    done_signal = pyqtSignal(name="done")

    def __init__(self, iface, my_mac, my_ip, first_ip, last_ip):
        super().__init__()
        self.iface = iface
        self.my_mac = my_mac
        self.my_ip = my_ip
        self.first_ip = first_ip
        self.last_ip = last_ip
        self.is_running = True

    def task(self):

        while self.is_running:
            for i in range(self.first_ip, self.last_ip + 1):
                dotted_ip = integer_to_dotted_decimal_ip(i)
                self.str_signal.emit(dotted_ip)
                send_data(self.iface, build_arp_query(self.my_mac, self.my_ip, i))
            self.is_running = False
            self.done_signal.emit()

    def stop(self):

        self.is_running = False

