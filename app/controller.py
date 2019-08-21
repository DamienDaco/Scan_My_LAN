# from PyQt5.QtGui import *
# from app.model import *
from app.table_view import *

from app.multithreading import *
from app.scapy_tools import *


class Controller:

    def __init__(self, view, model):

        self.default_interface = get_default_interface()
        self.selected_interface = self.default_interface
        self.interface_list = get_interfaces()
        self.get_selected_interface_info()

        self.model = model
        self.view = view
        self.view.set_controller(self)

        self.view.start()
        self.view.start_once()
        # self.view.create_table(self.model.host_list)
        self.query_threads = []
        self.scapy_sniffer_thread_list = []

        self.print_selected_interface()
        self.start_scapy_sniffer_thread()

        # self.model.create_sqlite_db()
        table_view_model = MySqlTableModel()
        table_view_model.setTable(self.model.db_table)
        table_view_model.setHeaderData(0, Qt.Horizontal, "IP Address")
        table_view_model.setHeaderData(1, Qt.Horizontal, "MAC Address")
        self.view.create_table_from_sql(table_view_model)

    def save_to_db(self, ip, mac):
        self.model.save_ip_mac_to_db(ip, mac)

    def get_selected_interface_info(self):
        self.my_mac = get_mac(self.selected_interface)
        self.my_ip = get_host_ip(self.selected_interface)
        self.my_mask = get_host_mask(self.selected_interface)

        self.hex_mac = hex_mac(self.my_mac)
        self.decimal_ip = decimal_ip(self.my_ip)

    def print_selected_interface(self):
        print("Your current interface is {}, your IP is {}, your mask is {} and your MAC is {}".format(
              self.selected_interface, self.my_ip, self.my_mask, self.my_mac))

    def calc_range(self):
        calc_range(self.my_ip, self.my_mask)

    def update_interface_box(self):
        iface = self.default_interface
        iface_list = self.interface_list
        return iface, iface_list

    def update_selected_interface(self):
        self.selected_interface = self.view.ui.interface_box.currentText()
        self.get_selected_interface_info()
        self.print_selected_interface()

    # @pyqtSlot(list) # <--- Do not use a pyqtSlot here, it breaks the connection
    # See https://stackoverflow.com/questions/40674940/why-does-pyqtslot-decorator-cause-typeerror-connect-failed
    def receive_data(self, data):
        print("received data", data)
        self.model.host_list = data

    def start_scapy_sniffer_thread(self):
        self.scapy_sniffer_worker = ScapyArpSnifferWorker(self.model.host_list)
        self.scapy_sniffer_thread = QThread()
        self.scapy_sniffer_thread_list.append((self.scapy_sniffer_worker, self.scapy_sniffer_thread))
        self.scapy_sniffer_worker.moveToThread(self.scapy_sniffer_thread)
        self.scapy_sniffer_worker.finished.connect(self.scapy_sniffer_thread.quit)
        self.scapy_sniffer_worker.send_list_signal.connect(self.receive_data)
        self.scapy_sniffer_thread.started.connect(self.scapy_sniffer_worker.task)
        self.scapy_sniffer_thread.start()

    def start_scapy_query_thread(self):
        if len(self.query_threads) > 0:
            self.view.ui.statusbar.showMessage("There's a query_thread already running. Please wait", 3000)
        else:
            self.first_ip, self.last_ip = calc_range(self.my_ip, self.my_mask)

            self.query_worker = ScapyArpQueryWorker(self.selected_interface, self.first_ip, self.last_ip)
            self.query_thread = QThread()
            self.query_threads.append((self.query_worker, self.query_thread))
            self.query_worker.moveToThread(self.query_thread)
            self.query_worker.finished.connect(self.query_thread.quit)
            self.query_thread.started.connect(self.query_worker.task)
            self.view.worker_connections()
            self.query_thread.start()

    # def start_query_thread(self):
    #
    #     if len(self.query_threads) > 0:
    #         self.view.ui.statusbar.showMessage("There's a query_thread already running. Please wait", 3000)
    #
    #     else:
    #         self.first_ip, self.last_ip = calc_range(self.my_ip, self.my_mask)
    #
    #         self.query_worker = ArpQueryWorker(self.default_interface, self.hex_mac, self.decimal_ip,
    #                                            self.first_ip, self.last_ip)
    #         self.query_thread = QThread()
    #         self.query_threads.append((self.query_worker, self.query_thread))
    #         self.query_worker.moveToThread(self.query_thread)
    #         self.query_thread.started.connect(self.query_worker.task)
    #         self.query_worker.done_signal.connect(self.stop_query_thread)
    #         self.query_worker.done_signal.connect(self.stop_arp_sniffer_thread)
    #
    #         self.query_thread.start()

    def stop_scapy_query(self):

        print("Stop button pressed")
        self.query_worker.stop_worker()

    def stop_query_thread(self):

        if len(self.query_threads) > 0:  # Check if there's something in the list
            print("Sending stop signal to query_thread")
            for worker, thread in self.query_threads:  # Let's go through the list of threads
                worker.stop_worker()  # And send the stop signal to each query_worker/query_thread
                thread.quit()
                thread.wait()

        self.query_threads = []  # When done, reset list

    # def start_arp_sniffer_thread(self):
    #     if len(self.arp_sniffer_thread_list) > 0:
    #         pass
    #     else:
    #         self.arp_sniffer_worker = ArpReplySnifferWorker(self.selected_interface, self.model.host_list)
    #         self.arp_sniffer_thread = QThread()
    #         self.arp_sniffer_thread_list.append((self.arp_sniffer_worker, self.arp_sniffer_thread))
    #         self.arp_sniffer_worker.moveToThread(self.arp_sniffer_thread)
    #         self.arp_sniffer_thread.started.connect(self.arp_sniffer_worker.task)
    #         self.arp_sniffer_thread.start()

    def stop_arp_sniffer_thread(self):
        for worker, thread in self.arp_sniffer_thread_list:
            worker.stop_worker()
            thread.quit()
            thread.wait()
        self.arp_sniffer_thread_list = []

