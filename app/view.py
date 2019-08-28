from PyQt5.QtCore import *
# from app.table_view import *


class View(QObject):

    def __init__(self, ui, ui_mainwindow):
        super().__init__()
        self.ui = ui
        self.ui_mainwindow = ui_mainwindow

    def set_controller(self, controller):
        self.controller = controller

    def start_once(self):
        self.update_interface_box()
        self.start_connections()

    def start_connections(self):
        self.ui.scan_button.clicked.connect(self.controller.start_scapy_query_thread)
        # self.ui.start_button.clicked.connect(self.controller.start_arp_sniffer_thread) #No longer necessary because of Scapy
        # self.ui.debug_button.clicked.connect(lambda: self.controller.save_to_db('192.168.1.1', 'aa:bb:cc:11:22:33'))
        self.ui.interface_box.currentIndexChanged.connect(self.controller.update_selected_interface)
        # self.ui.debug_button.clicked.connect(lambda: self.controller.check_if_record_exists('192.168.1.1'))

    def worker_connections(self):
        self.ui.stop_button.clicked.connect(lambda: self.controller.stop_query_thread())

    def start(self):
        pass

    def update_interface_box(self):
        iface, iface_list = self.controller.update_interface_box()
        self.ui.interface_box.addItems(iface_list)
        self.ui.interface_box.setCurrentText(iface)