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



