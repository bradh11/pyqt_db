"""
Update a query in a table view.  

To make the QSqlQueryModel read/write you must subclass it and reimplement the setData() and flags()
methods.  

The Qt querymodel example shows how to do this.  
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

        if index.column() in (1, 3):
            flags |= Qt.ItemIsEditable

        return flags

    def setData(self, index, value, role):
        if index.column() not in (1, 3):
            return False

        LineID_index = self.index(index.row(), 0)
        BranchID_index = self.index(index.row(), 2)
        LineID = self.data(LineID_index)
        BranchID = self.data(BranchID_index)

        self.clear()

        if index.column() == 1:
            ok = self.setLineName(LineID, value)
        elif index.column() == 3:
            ok = self.setBranchName(BranchID, value)
        else:
            raise Exception("Oops")

        self.refresh()
        return ok

    def refresh(self):
        sql = dedent("""\
                SELECT line.LineID, line.LineName, branch.BranchID, branch.BranchName FROM line
                INNER JOIN branch 
                        ON branch.LineID = line.LineID
                """)

        self.setQuery(sql)
        self.setHeaderData(0, Qt.Horizontal, "LineID")
        self.setHeaderData(1, Qt.Horizontal, "LineName")
        self.setHeaderData(2, Qt.Horizontal, "BranchID")
        self.setHeaderData(3, Qt.Horizontal, "BranchName")

    def setLineName(self, LineID, LineName):
        query = QSqlQuery()
        query.prepare('update line set LineName= ? where LineID = ?')
        query.addBindValue(LineName)
        query.addBindValue(LineID)
        return query.exec_()

    def setBranchName(self, BranchID, BranchName):
        query = QSqlQuery()
        query.prepare('update branch set BranchName = ? where BranchID = ?')
        query.addBindValue(BranchName)
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

        # Initialize Model
        sql = dedent("""\
                SELECT line.LineID, line.LineName, branch.BranchID, branch.BranchName FROM line
                INNER JOIN branch 
                        ON branch.LineID = line.LineID
                """)
        model = EditableSqlModel()
        model.setQuery(sql)
        model.setHeaderData(0, QtCore.Qt.Horizontal, "LineID")
        model.setHeaderData(1, QtCore.Qt.Horizontal, "LineName")
        model.setHeaderData(2, QtCore.Qt.Horizontal, "BranchID")
        model.setHeaderData(3, QtCore.Qt.Horizontal, "BranchName")

        # Create View
        view = self.ui.tableView
        view.setModel(model)
        view.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())