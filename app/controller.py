# from PyQt5.QtGui import *
# from app.model import *

from app.multithreading import *


class Controller:

    def __init__(self, view, model):

        self.model = model
        self.view = view
        self.view.set_controller(self)

        self.view.start()
        self.view.start_once()
        self.query_threads = []
        self.arp_sniffer_thread_list = []
        self.print_selected_interface()

    def print_selected_interface(self):
        print("Your current interface is {}, your IP is {}, your mask is {} and your MAC is {}".format(
              self.model.selected_interface, self.model.my_ip, self.model.my_mask, self.model.my_mac))

    def calc_range(self):
        calc_range(self.model.my_ip, self.model.my_mask)

    def update_interface_box(self):
        iface = self.model.default_interface
        iface_list = self.model.interface_list
        return iface, iface_list

    def update_selected_interface(self):
        self.model.selected_interface = self.view.ui.interface_box.currentText()
        self.model.get_selected_interface_info()
        self.print_selected_interface()

    def start_query_thread(self):

        if len(self.query_threads) > 0:
            self.view.ui.statusbar.showMessage("There's a query_thread already running. Please wait", 3000)

        else:
            self.first_ip, self.last_ip = calc_range(self.model.my_ip, self.model.my_mask)

            self.query_worker = ArpQueryWorker(self.model.default_interface, self.model.hex_mac, self.model.decimal_ip,
                                               self.first_ip, self.last_ip)
            self.query_thread = QThread()
            self.query_threads.append((self.query_worker, self.query_thread))
            self.query_worker.moveToThread(self.query_thread)
            self.query_thread.started.connect(self.query_worker.task)
            self.query_worker.done_signal.connect(self.stop_query_thread)
            self.query_worker.done_signal.connect(self.stop_arp_sniffer_thread)
            self.query_thread.start()

    def stop_query_thread(self):

        if len(self.query_threads) > 0:  # Check if there's something in the list
            print("Sending stop signal to query_thread")
            for worker, thread in self.query_threads:  # Let's go through the list of threads
                worker.stop()  # And send the stop signal to each query_worker/query_thread
                thread.quit()
                thread.wait()

        self.query_threads = []  # When done, reset list

    def start_arp_sniffer_thread(self):
        if len(self.arp_sniffer_thread_list) > 0:
            pass
        else:
            self.arp_sniffer_worker = ArpReplySnifferWorker(self.model.selected_interface, self.model.host_list)
            self.arp_sniffer_thread = QThread()
            self.arp_sniffer_thread_list.append((self.arp_sniffer_worker, self.arp_sniffer_thread))
            self.arp_sniffer_worker.moveToThread(self.arp_sniffer_thread)
            self.arp_sniffer_thread.started.connect(self.arp_sniffer_worker.task)
            self.arp_sniffer_thread.start()

    def stop_arp_sniffer_thread(self):
        for worker, thread in self.arp_sniffer_thread_list:
            worker.stop()
            thread.quit()
            thread.wait()
        self.arp_sniffer_thread_list = []

