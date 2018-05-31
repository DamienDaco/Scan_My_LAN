import sys
from app.model import *
from ui.gui import *
from app.view import *
from app.controller import *
from PyQt5.QtWidgets import *
# from PyQt5.QtWidgets import


if __name__ == "__main__":

    app = QApplication(sys.argv)

    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    model = Model()
    view = View(ui, MainWindow)
    controller = Controller(view, model)
    sys.exit(app.exec_())