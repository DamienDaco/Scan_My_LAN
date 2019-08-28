from app.multithreading import *
import os, pickle
from PyQt5.QtSql import *
from app.table_view import *


class Model:

    def __init__(self):
        super().__init__()

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
                                "mac_address TEXT NOT NULL, oui TEXT, status TEXT)"):
            print(self.query.lastError().text())

        self.table_view_model = MySqlTableModel()
        self.table_view_model.setTable(self.db_table)
        self.table_view_model.select()

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
        if not self.query.exec_():
            print("Ooops")
            print(self.query.lastError().text())
            return False
        while self.query.next():
            print(self.query.value(0))
        print(self.query.lastError().text())

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



