from PyQt5.QtCore import *
from app.network_functions import *

from ui.gui import *


class View(QObject):

    def __init__(self, ui, ui_mainwindow):
        super().__init__()
        self.ui = ui
        self.ui_mainwindow = ui_mainwindow

        # self.start_once()
        # self.start_connections()

    def set_controller(self, controller):
        self.controller = controller

    def start_once(self):
        self.start_connections()

    def start_connections(self):
        self.ui.start_button.clicked.connect(self.controller.start_query_thread)
        self.ui.debug_button.clicked.connect(lambda: print("Test"))

    def start(self):
        pass