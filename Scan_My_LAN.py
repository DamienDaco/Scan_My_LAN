import sys
from app.logic import *
from PyQt5.QtWidgets import QApplication


if __name__ == "__main__":

    app = QApplication(sys.argv)
    logic = Logic()
    sys.exit(app.exec_())