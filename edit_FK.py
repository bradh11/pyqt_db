"""
Edit a foreign key and enforce integrity.  In this case FromBusID and ToBusID can only be set to values that 
already exist in the bus table.
"""
import sql_example_ui
from PyQt5.QtCore import Qt
from PyQt5 import QtCore
from PyQt5.QtWidgets import (QMainWindow, QApplication)
from PyQt5 import QtSql
from PyQt5.QtSql import (QSqlQuery, QSqlQueryModel)
import sys
from textwrap import dedent


class EditableSqlModel(QtSql.QSqlQueryModel):

    def flags(self, index):
        flags = super(EditableSqlModel, self).flags(index)

        if index.column() in (1, 2, 3):
            flags |= Qt.ItemIsEditable

        return flags

    def setData(self, index, value, role):
        if index.column() not in (1, 2, 3):
            return False

        BranchID_index = self.index(index.row(), 0)
        BranchID = self.data(BranchID_index)

        self.clear()

        if index.column() == 1:
            ok = self.setBranchName(BranchID, value)
        elif index.column() == 2:
            ok = self.setFromBus(BranchID, value)
        elif index.column() == 3:
            ok = self.setToBus(BranchID, value)
        else:
            raise Exception("Oops")

        self.refresh()
        return ok

    def refresh(self):
        sql = dedent("""\
                SELECT branch.BranchID, branch.BranchName, FromBus.BusID AS FromBusID, ToBus.BusID AS ToBusID
                FROM branch
                INNER JOIN bus AS FromBus 
                        ON FromBus.BusID = branch.FromBusID
                INNER JOIN bus AS ToBus 
                        ON ToBus.BusID = branch.ToBusID
                """)

        self.setQuery(sql)
        self.setHeaderData(0, Qt.Horizontal, "BranchID")
        self.setHeaderData(1, Qt.Horizontal, "BranchName")
        self.setHeaderData(2, Qt.Horizontal, "FromBusID")
        self.setHeaderData(3, Qt.Horizontal, "ToBusID")

    def setBranchName(self, BranchID, BranchName):
        query = QSqlQuery()
        query.prepare('update branch set BranchName = ? where BranchID = ?')
        query.addBindValue(BranchName)
        query.addBindValue(BranchID)
        return query.exec_()

    def setFromBus(self, BranchID, FromBusID):
        query = QSqlQuery()
        query.prepare('update branch set FromBusID = ? where BranchID = ?')
        query.addBindValue(FromBusID)
        query.addBindValue(BranchID)
        return query.exec_()

    def setToBus(self, BranchID, ToBusID):
        query = QSqlQuery()
        query.prepare('update branch set ToBusID = ? where BranchID = ?')
        query.addBindValue(ToBusID)
        query.addBindValue(BranchID)
        return query.exec_()


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = sql_example_ui.Ui_MainWindow()
        self.ui.setupUi(self)

        db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName('example.sqlite')
        db.open() # This is important sometimes
        query = QSqlQuery()
        query.prepare('PRAGMA foreign_keys = ON;')
        query.exec_()

        # Initialize Model
        sql = dedent("""\
                SELECT branch.BranchID, branch.BranchName, FromBus.BusID AS FromBusID, ToBus.BusID AS ToBusID
                FROM branch
                INNER JOIN bus AS FromBus 
                        ON FromBus.BusID = branch.FromBusID
                INNER JOIN bus AS ToBus 
                        ON ToBus.BusID = branch.ToBusID
                """)

        model = EditableSqlModel()
        model.setQuery(sql)
        model.setHeaderData(0, Qt.Horizontal, "BranchID")
        model.setHeaderData(1, Qt.Horizontal, "BranchName")
        model.setHeaderData(2, Qt.Horizontal, "FromBusID")
        model.setHeaderData(3, Qt.Horizontal, "ToBusID")

        # Create View
        view = self.ui.tableView
        view.setModel(model)
        view.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
