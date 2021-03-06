from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from app.network_functions import *

'''
Warning: This whole file has become obsolete. See file scapy_tools.py for new updated classes.
'''


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


class ArpReplySnifferWorker(QObject):
    done_signal = pyqtSignal(object)

    def __init__(self, interface, host_list):

        super().__init__()
        self.is_running = True
        self.interface = interface
        self.host_list = host_list

    def task(self):
        print("Capturing ARP replies on interface {}".format(self.interface))

        while self.is_running:

            sniff_arp(self.interface, self.host_list)

        self.done_signal.emit(self.host_list)

    @pyqtSlot()
    def stop(self):
        print("Sniffer worker received stop signal")
        self.is_running = False
