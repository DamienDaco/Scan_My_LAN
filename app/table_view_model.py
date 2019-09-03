from PyQt5.QtCore import *
from PyQt5.QtSql import *
from PyQt5.QtGui import *


class CustomSortingModel(QSortFilterProxyModel):
    """
    Custon proxy model between view and model to sort IP addresses by their int (numerical) value.
    lessThan() will override the sorting function in QSortFilterProxyModel.
    Allows to sort IP addresses which were strings ('192.168.1.1') by their numerical value.
    In this example, col == 1 because this is my column for IP addresses in my model.
    int(dataleft.split('.')[0]).... etc: This will create a tuple of four octets, e.g. (192, 168, 1, 1)
    These tuples of octets will be sorted by numerical value.
    """
    def lessThan(self, left, right):

        col = left.column()

        left_data = left.data()
        right_data = right.data()
        if left_data and right_data:  # Important: Check if the string is not empty before using it
            if col == 1:  # Column for IP addresses in my model
                left_data = (int(left_data.split('.')[0]), int(left_data.split('.')[1]), int(left_data.split('.')[2]),
                             int(left_data.split('.')[3]))
                right_data = (int(right_data.split('.')[0]), int(right_data.split('.')[1]), int(right_data.split('.')[2]),
                              int(right_data.split('.')[3]))
        return left_data < right_data


class MySqlTableModel(QSqlTableModel):
    def __init__(self):
        super(MySqlTableModel, self).__init__()
        self.setEditStrategy(QSqlTableModel.OnManualSubmit)

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
