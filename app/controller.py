from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
# from app.model import *
from app.table_view_model import *
from app.scapy_tools import *
from app.view import *
from manuf import manuf


class Controller(QObject):
    send_ip_signal = pyqtSignal(str)

    def __init__(self, view, model):
        super().__init__()

        self.default_interface = get_default_interface()
        self.selected_interface = self.default_interface
        self.interface_list = get_interfaces_with_scapy()
        self.model = model
        self.view = view
        self.view.set_controller(self)

        self.view.start()
        self.view.start_once()

        self.query_threads = []
        self.scapy_sniffer_thread_list = []

        self.get_selected_interface_info()
        self.print_selected_interface()
        self.start_scapy_sniffer_thread()
        self.start_fqdn_thread()

        self.view.ui.table_view.setModel(self.model.table_view_model)
        self.view.ui.table_view.setColumnHidden(0, True)  # Hides the id column
        self.view.ui.table_view.setEditTriggers(QAbstractItemView.NoEditTriggers) # Set table view to read only

        self.mac_parser = manuf.MacParser(update=False)

    def add_ip_mac_in_db(self, ip, mac):
        """
        Parameters:
        argument1 (str): e.g. '192.168.1.1'

        argument2 (str): e.g. '11:22:33:AA:BB:CC'

        Why should we use record.setGenerated('id', False) ?
        Because we're using Sqlite auto incremented primary key; the database itself will provide that value.
        If we don't set it to False, all the fields turn up empty.
        https://stackoverflow.com/a/42319334/6743356
        The caller should remember to set the generated flag to FALSE for fields where the database is meant to supply the value,
         such as an automatically incremented ID.
        """

        if not ([i for i in range(self.model.table_view_model.rowCount())
                if ip == (self.model.table_view_model.record(i).value('ip_address'))]):
            print("Could not find record {} in db".format(ip))
            print("Adding IP {} and MAC {} to db".format(ip, mac))
            oui = self.mac_parser.get_manuf_long(mac)
            record = self.model.table_view_model.record()
            record.setValue('ip_address', ip)
            record.setValue('mac_address', mac)
            record.setValue('oui', oui)
            record.setGenerated('id', False)
            self.model.table_view_model.insertRecord(-1, record)
            self.send_ip_signal.emit(ip)

        else:
            for i in range(self.model.table_view_model.rowCount()):
                if (ip == (self.model.table_view_model.record(i).value('ip_address'))
                        and mac != (self.model.table_view_model.record(i).value('mac_address'))):

                    print("Updating MAC address for host {} with new value {}".format(ip, mac))
                    # record = self.model.table_view_model.record()
                    oui = self.mac_parser.get_manuf_long(mac)
                    record = self.model.table_view_model.record(i)
                    record.setValue('mac_address', mac)
                    record.setValue('oui', oui)
                    self.model.table_view_model.setRecord(i, record)
                    self.send_ip_signal.emit(ip)

    def add_fqdn_to_db(self, ip, fqdn):
        """
                Parameters:
                argument1 (str): e.g. '192.168.1.1'

                argument2 (str): e.g. 'fritz.box'
        """
        print("Adding FQDN {} for host {} to db".format(fqdn, ip))
        # for i in range(self.model.table_view_model.rowCount()):
        #     if ip == (self.model.table_view_model.record(i).value('ip_address')):
        #         if not(self.model.table_view_model.record(i).value('computer_name')):
        #             record = self.model.table_view_model.record(i)
        #             record.setValue('computer_name', fqdn)
        #             self.model.table_view_model.setRecord(i, record)
        if ip == fqdn:
            '''Some computers/devices don't have a network name. 
            In that case, getfqdn() returns the IP as the FQDN value. Therefore, let's ignore it.'''
            pass
        else:
            query = QSqlQuery()
            query.prepare("UPDATE live_hosts SET computer_name = :fqdn WHERE ip_address = :ip")
            query.bindValue(":fqdn", fqdn)
            query.bindValue(":ip", ip)
            if query.exec_():
                self.model.table_view_model.select()
            else:
                print(query.lastError().text())


        # if ([((record = self.model.table_view_model.setRecord(i).setValue('computer_name', fqdn)), self.model.table_view_model.record(i, record))
        #                                             )) for i in range(self.model.table_view_model.rowCount())
        #         if not (self.model.table_view_model.record(i).value('computer_name'))]):
        #     print("Can't find record {} for IP {}".format(fqdn, ip))
        #
        # else:
        #     print("Found record {} for IP {}".format(fqdn, ip))

    # def add_record_to_db(self, ip, mac):
    #     print("Adding IP {} and MAC {} to db".format(ip, mac))
    #     record = self.table_view_model.record()
    #     record.setValue('ip_address', ip)
    #     record.setValue('mac_address', mac)
    #     record.setGenerated('id', False)
    #     self.table_view_model.insertRecord(-1, record)

    def get_selected_interface_info(self):
        self.my_mac = get_mac(self.selected_interface)
        self.my_ip = get_host_ip(self.selected_interface)
        self.my_mask = get_host_mask(self.selected_interface)

        self.hex_mac = hex_mac(self.my_mac)
        self.decimal_ip = decimal_ip(self.my_ip)

    def print_selected_interface(self):
        print("Your current interface is {}, your IP is {}, your mask is {} and your MAC is {}".format(
              self.view.ui.interface_box.currentText(), self.my_ip, self.my_mask, self.my_mac))

    def calc_range(self):
        calc_range(self.my_ip, self.my_mask)

    def update_interface_box(self):
        iface = self.default_interface
        iface_list = self.interface_list
        return iface, iface_list

    def update_selected_interface(self):
        idx = self.view.ui.interface_box.currentIndex()
        self.selected_interface = get_interfaces()[idx]
        self.get_selected_interface_info()
        self.print_selected_interface()

    # @pyqtSlot(list) # <--- Do not use a pyqtSlot here, it breaks the connection
    # See https://stackoverflow.com/questions/40674940/why-does-pyqtslot-decorator-cause-typeerror-connect-failed
    def receive_data(self, data1, data2):
        print("Received data {} and {}".format(data1, data2))
        # self.model.host_list = data

    def debug_fqdn(self, ip, fqdn):
        print("Received IP {} and FQDN {}".format(ip, fqdn))

    def debug_signal(self, signal):
        print("Received signal {}".format(signal))

    def start_scapy_sniffer_thread(self):
        self.scapy_sniffer_worker = ScapyArpSnifferWorker()
        self.scapy_sniffer_thread = QThread()
        self.scapy_sniffer_thread_list.append((self.scapy_sniffer_worker, self.scapy_sniffer_thread))
        self.scapy_sniffer_worker.moveToThread(self.scapy_sniffer_thread)
        self.scapy_sniffer_worker.finished.connect(self.scapy_sniffer_thread.quit)
        self.scapy_sniffer_worker.send_list_signal.connect(self.add_ip_mac_in_db)
        self.scapy_sniffer_thread.started.connect(self.scapy_sniffer_worker.task)
        self.scapy_sniffer_thread.start()

    def start_scapy_query_thread(self):
        if len(self.query_threads) > 0:
            self.view.ui.statusbar.showMessage("There's a query_thread already running. Please wait", 3000)
        else:
            self.first_ip, self.last_ip = calc_range(self.my_ip, self.my_mask)

            self.query_worker = ScapyArpQueryWorker(self.selected_interface, self.first_ip, self.last_ip)
            self.query_thread = QThread()
            self.query_threads.append((self.query_worker, self.query_thread))
            self.query_worker.moveToThread(self.query_thread)
            self.query_worker.finished.connect(self.query_thread.quit)
            self.query_thread.started.connect(self.query_worker.task)
            self.view.worker_connections()
            self.query_thread.start()

    def start_fqdn_thread(self):
        self.fqdn_worker = FqdnWorker()
        self.fqdn_thread = QThread()
        self.fqdn_worker.moveToThread(self.fqdn_thread)
        # self.fqdn_thread.started.connect(self.fqdn_worker.task) # Don't start it yet
        # self.scapy_sniffer_worker.send_ip_signal.connect(self.fqdn_worker.task)
        # self.scapy_sniffer_worker.send_ip_signal.connect(self.fqdn_worker.task)
        self.fqdn_worker.send_fqdn_signal.connect(self.add_fqdn_to_db)
        self.send_ip_signal.connect(self.fqdn_worker.task)
        self.fqdn_thread.start()

    def stop_scapy_query(self):

        print("Stop button pressed")
        self.query_worker.stop_worker()

    def stop_query_thread(self):

        if len(self.query_threads) > 0:  # Check if there's something in the list
            print("Sending stop signal to query_thread")
            for worker, thread in self.query_threads:  # Let's go through the list of threads
                worker.stop_worker()  # And send the stop signal to each query_worker/query_thread
                thread.quit()
                thread.wait()

        self.query_threads = []  # When done, reset list

    def stop_arp_sniffer_thread(self):
        for worker, thread in self.arp_sniffer_thread_list:
            worker.stop_worker()
            thread.quit()
            thread.wait()
        self.arp_sniffer_thread_list = []

