from PyQt5.QtCore import *


class View(QObject):

    def __init__(self, ui, ui_mainwindow):
        super().__init__()
        self.ui = ui
        self.ui_mainwindow = ui_mainwindow

    def set_controller(self, controller):
        self.controller = controller

    def start_once(self):
        self.start_connections()
        self.update_interface_box()

    def start_connections(self):
        self.ui.start_button.clicked.connect(self.controller.start_query_thread)
        self.ui.debug_button.clicked.connect(lambda: print("Test"))

    def start(self):
        pass

    def update_interface_box(self):
        iface, iface_list = self.controller.update_interface_box()
        self.ui.interface_box.addItems(iface_list)
        self.ui.interface_box.setCurrentText(iface)
