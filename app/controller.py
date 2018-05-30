# from PyQt5.QtGui import *
# from app.model import *

from app.multithreading import *


class Controller:

    def __init__(self, view, model):

        self.model = model
        self.view = view
        self.view.set_controller(self)

        self.view.start()
        self.view.start_connections()
        self.query_threads = []

    def calc_range(self):

        calc_range(self.model.my_ip, self.model.my_mask)

    def start_query_thread(self):

        if len(self.query_threads) > 0:
            self.view.ui.statusbar.showMessage("There's a thread already running. Please wait", 3000)

        else:
            self.first_ip, self.last_ip = calc_range(self.model.my_ip, self.model.my_mask)

            self.worker = ArpQueryWorker(self.model.default_interface, self.model.hex_mac, self.model.decimal_ip,
                                         self.first_ip, self.last_ip)
            self.thread = QThread()
            self.query_threads.append((self.worker, self.thread))
            self.worker.moveToThread(self.thread)
            self.thread.started.connect(self.worker.task)
            self.worker.done_signal.connect(self.stop_thread)
            self.thread.start()

    def stop_thread(self):

        if len(self.query_threads) > 0:  # Check if there's something in the list
            print("Sending stop signal to thread")
            for worker, thread in self.query_threads:  # Let's go through the list of threads
                worker.stop()  # And send the stop signal to each worker/thread
                thread.quit()
                thread.wait()

        self.query_threads = []  # When done, reset list


