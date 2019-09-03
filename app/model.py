from app.multithreading import *
import os, pickle
from PyQt5.QtSql import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from app.table_view_model import *
from manuf import manuf


class Model(QObject):
    send_ip_signal = pyqtSignal(str)

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
        if not self.query.exec_("DROP TABLE IF EXISTS live_hosts"):
            print(self.query.lastError().text())
        if not self.query.exec_("CREATE TABLE IF NOT EXISTS live_hosts(id INTEGER PRIMARY KEY,"
                                "ip_address TEXT NOT NULL UNIQUE, "
                                "mac_address TEXT NOT NULL, oui TEXT, status TEXT,"
                                "computer_name TEXT, user_text TEXT)"):
            print(self.query.lastError().text())

        self.table_view_model = MySqlTableModel()
        self.table_view_model.setTable(self.db_table)
        self.table_view_model.setHeaderData(1, Qt.Horizontal, "IP Address")
        self.table_view_model.setHeaderData(2, Qt.Horizontal, "MAC Address")
        self.table_view_model.setHeaderData(3, Qt.Horizontal, "Manufacturer")
        self.table_view_model.setHeaderData(4, Qt.Horizontal, "Status")
        self.table_view_model.setHeaderData(5, Qt.Horizontal, "Computer Name")
        self.table_view_model.setHeaderData(6, Qt.Horizontal, "User Text")
        self.table_view_model.select()

        self.proxy_model = CustomSortingModel()
        self.proxy_model.setSourceModel(self.table_view_model)

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

        if not ([i for i in range(self.table_view_model.rowCount())
                 if ip == (self.table_view_model.record(i).value('ip_address'))]):
            print("Could not find record {} in db".format(ip))
            print("Adding IP {} and MAC {} to db".format(ip, mac))
            oui = self.mac_parser.get_manuf_long(mac)
            print("MAC {} manufacturer = {}".format(mac, oui))
            record = self.table_view_model.record()
            record.setValue('ip_address', ip)
            record.setValue('mac_address', mac)
            record.setValue('oui', oui)
            record.setGenerated('id', False)
            if not self.table_view_model.insertRecord(-1, record):
                print("Insert in db failed!")
                print(self.table_view_model.lastError().text())
                self.table_view_model.revertAll()
            else:
                self.table_view_model.submitAll()
            self.send_ip_signal.emit(ip)

        else:
            for i in range(self.table_view_model.rowCount()):
                if (ip == (self.table_view_model.record(i).value('ip_address'))
                        and mac != (self.table_view_model.record(i).value('mac_address'))):
                    print("Updating MAC address for host {} with new value {}".format(ip, mac))
                    # record = self.model.table_view_model.record()
                    oui = self.mac_parser.get_manuf_long(mac)
                    record = self.table_view_model.record(i)
                    record.setValue('mac_address', mac)
                    record.setValue('oui', oui)
                    if not self.table_view_model.setRecord(i, record):
                        print("Update MAC in db failed!")
                        print(self.table_view_model.lastError().text())
                        self.table_view_model.revertAll()
                    else:
                        self.table_view_model.submitAll()
                    self.send_ip_signal.emit(ip)

    def add_fqdn_to_db(self, ip, fqdn):
        """
                Parameters:
                argument1 (str): e.g. '192.168.1.1'

                argument2 (str): e.g. 'fritz.box'
        """
        print("Adding FQDN {} for host {} to db".format(fqdn, ip))
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
                self.table_view_model.select()
            else:
                print(query.lastError().text())



