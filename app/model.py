from app.multithreading import *
import os, pickle
from PyQt5.QtSql import *


class Model:

    def __init__(self):
        super().__init__()

        # self.default_interface = get_default_interface()
        # self.selected_interface = self.default_interface
        # self.interface_list = get_interfaces()
        # self.get_selected_interface_info()

        self.host_list = []
        self.db = QSqlDatabase.addDatabase('QSQLITE')
        if not self.db.isValid():
            print("Error: Invalid database.")

        self.db.setDatabaseName('live_hosts.db')
        if not self.db.open():
            print("Error {}".format(self.db.lastError().text()))
        self.db_table = 'live_hosts'

        self.query = QSqlQuery()
        if not self.query.exec_("CREATE TABLE IF NOT EXISTS live_hosts(id INTEGER PRIMARY KEY,"
                                "ip_address TEXT NOT NULL UNIQUE, "
                                "mac_address TEXT NOT NULL, oui TEXT)"):
            print(self.query.lastError().text())

        # This was just for debugging:
        # if not query.prepare("INSERT INTO live_hosts values('192.168.1.1', "
        #                      "'e0:28:6d:2c:e8:9f')"):
        #     print(db.lastError().text())
        #     return False
        # if not self.query.exec_("INSERT INTO live_hosts (ip_address, mac_address, oui) VALUES('192.168.1.1', 'e0:28:6d:AA:BB:EE', 'Asus')"):
        #     print(self.query.lastError().text())

        print(self.query.lastError().text())
        self.query.clear()

    def save_ip_mac_to_db(self, ip, mac):
        print("Attempting to save to db")
        self.query.prepare("INSERT INTO live_hosts (ip_address, mac_address)"
                           "VALUES (?, ?)")
        self.query.addBindValue(ip)
        self.query.addBindValue(mac)
        if not self.query.exec_():
            print(self.query.lastError().text())
            return False
        while self.query.next():
            print(self.query.value(0))

    def update_db(self):
        print("Attempting to update db:")

        self.query = QSqlQuery()

        self.query.prepare("SELECT EXISTS(SELECT 1 FROM live_hosts WHERE ip_address='192.168.1.154')")
        # self.query.addBindValue('192.168.1.1')
        # print("query.isActive is".format(self.query.isActive()))
        if not self.query.exec_():
            print("Ooops")
            print(self.query.lastError().text())
            return False
        while self.query.next():
            print(self.query.value(0))
        print(self.query.lastError().text())
        # print("Query.size is".format(self.query.size()))

    def open_pickled_list(self):
        try:
            with open('live_hosts.data', 'rb') as f:
                self.host_list = pickle.load(f)
        except Exception:
            print("Couldn't load list of hosts.")

    def pickle_list_to_disk(self):
        try:
            with open('live_hosts.data', 'wb') as f:
                pickle.dump(self.host_list, f)
        except Exception:
            print("Couldn't save list to disk")

    # def get_selected_interface_info(self):
    #     self.my_mac = get_mac(self.selected_interface)
    #     self.my_ip = get_host_ip(self.selected_interface)
    #     self.my_mask = get_host_mask(self.selected_interface)
    #
    #     self.hex_mac = hex_mac(self.my_mac)
    #     self.decimal_ip = decimal_ip(self.my_ip)



