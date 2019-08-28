from PyQt5.QtCore import *
from PyQt5.QtSql import *
from PyQt5.QtGui import *


class MySqlTableModel(QSqlTableModel):
    def __init__(self):
        super(MySqlTableModel, self).__init__()

        self.setEditStrategy(QSqlTableModel.OnFieldChange)
        self.setHeaderData(1, Qt.Horizontal, "IP Address")
        self.setHeaderData(2, Qt.Horizontal, "MAC Address")
        self.setHeaderData(3, Qt.Horizontal, "Manufacturer")
        self.setHeaderData(4, Qt.Horizontal, "Status")

    def info(self):
        print("-> info")
        print("   MySqlTableModel tables inside :", self.database().tables())
        print("   MySqlTableModel self.db       :", self.database())
        print("   MySqlTableModel self.Table    :", self.tableName())
        print("   MySqlTableModel self.rowCount :", self.rowCount())
        print("   MySqlTableModel self.lastError :", self.lastError().text())
        print("<- info")


class MyTableModel(QAbstractTableModel):
    def __init__(self, datain, headerdata, parent=None):
        '''
            This model is now obsolete.
            It used to be my table model when I was using a list of dictionaries.
            No longer used. See 'MySqlTableModel' for current model.
        '''
        super(MyTableModel, self).__init__(parent)
        self.arraydata = datain
        self.headerdata = headerdata

    def rowCount(self, parent):
        return len(self.arraydata)

    def columnCount(self, parent):
        if len(self.arraydata) > 0:
            return len(self.arraydata[0])
        return 0

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            i = index.row()
            j = index.column()
            # lst = [[(k, v) for k, v in d.items()] for d in self.arraydata]
            return '{}'.format([[(k, v) for k, v in d.items()] for d in self.arraydata][i][j][1])
        else:
            return None

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return QVariant(self.headerdata[col])
        return QVariant()

    def flags(self, index):
        return Qt.ItemIsEnabled

    # def sort(self, Ncol, order):
    #     """Sort table by given column number.
    #     """
    #     self.emit(SIGNAL("layoutAboutToBeChanged()"))
    #     self.arraydata = sorted(self.arraydata, key=operator.itemgetter(Ncol))
    #     if order == Qt.DescendingOrder:
    #         self.arraydata.reverse()
    #     self.emit(SIGNAL("layoutChanged()"))
