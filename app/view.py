from PyQt5.QtCore import *


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
        self.ui.start_button.clicked.connect(self.controller.start_scapy_worker_thread)
        # self.ui.start_button.clicked.connect(self.controller.start_arp_sniffer_thread) #No longer necessary because of Scapy
        self.ui.debug_button.clicked.connect(lambda: print("Test"))
        self.ui.interface_box.currentIndexChanged.connect(self.controller.update_selected_interface)

    def start(self):
        pass

    def update_interface_box(self):
        iface, iface_list = self.controller.update_interface_box()
        self.ui.interface_box.addItems(iface_list)
        self.ui.interface_box.setCurrentText(iface)
