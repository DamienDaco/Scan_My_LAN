# from PyQt5.QtGui import *
# from app.model import *
from app.network_functions import *


class Controller:

    def __init__(self, view, model):

        self.model = model
        self.view = view
        self.view.set_controller(self)

        self.view.start()

    def calc_range(self):

        calc_range(self.model.my_ip, self.model.my_mask)

