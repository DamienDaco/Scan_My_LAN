import sys
from app.model import *
from ui.gui import *
from app.view import *
from app.controller import *
from PyQt5.QtWidgets import *
# from PyQt5.QtWidgets import


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()


if __name__ == "__main__":

    app = QApplication(sys.argv)

    my_app = MainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(my_app)
    my_app.show()
    model = Model()
    view = View(ui, my_app)
    controller = Controller(view, model)
    sys.exit(app.exec_())