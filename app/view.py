from PyQt5.QtCore import *
from app.table_view import *
from PyQt5.QtSql import *


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
        # self.create_table()

    def start_connections(self):
        self.ui.scan_button.clicked.connect(self.controller.start_scapy_query_thread)
        # self.ui.start_button.clicked.connect(self.controller.start_arp_sniffer_thread) #No longer necessary because of Scapy
        self.ui.debug_button.clicked.connect(lambda: print("Test"))
        self.ui.interface_box.currentIndexChanged.connect(self.controller.update_selected_interface)

    def worker_connections(self):
        self.ui.stop_button.clicked.connect(lambda: self.controller.stop_query_thread())

    def start(self):
        pass

    def update_interface_box(self):
        iface, iface_list = self.controller.update_interface_box()
        self.ui.interface_box.addItems(iface_list)
        self.ui.interface_box.setCurrentText(iface)

    # def create_table(self, table_data):
    #     # table_data = ['1', '2', '3', '4']
    #     header = ['IP Address', 'MAC Address']
    #     tm = MyTableModel(table_data, header, self)
    #     self.ui.table_view.setModel(tm)

    def create_table_from_sql(self):
        tm = QSqlTableModel()
        tm.setTable('live_hosts')
        tm.select()
        self.ui.table_view.setModel(tm)
