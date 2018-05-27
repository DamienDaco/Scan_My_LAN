import sys
from app.model import *
from PyQt5.QtWidgets import QApplication


if __name__ == "__main__":

    app = QApplication(sys.argv)
    model = Model()
    sys.exit(app.exec_())