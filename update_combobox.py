"""
Use a combobox to display valid values for the bus fields.  The valid values are based purely on the 
table relationships.  

I want a couple enhancements:
  - restrict valid values based on a query which only present the user items based
    on a certain criteria.
"""
import sql_example_ui
from PyQt5.QtCore import Qt
from PyQt5 import QtCore
from PyQt5.QtGui import QStandardItem, QStandardItemModel
from PyQt5.QtWidgets import (QMainWindow, QApplication, QItemDelegate, QComboBox, QTableView)
from PyQt5 import QtSql
from PyQt5.QtSql import (QSqlQuery, QSqlQueryModel, QSqlRelationalTableModel, QSqlTableModel, QSqlRelation, QSqlRelationalDelegate)
import sys

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

        model = QSqlRelationalTableModel()
        #sql = "SELECT branch.BranchID, branch.BranchName, FromBusID, ToBusID FROM branch;"
        model.setTable('branch')
        #model.setQuery(QSqlQuery(sql))
        model.setEditStrategy(QSqlTableModel.OnFieldChange)

        # Instead of FromBusID show the BusName
        model.setRelation(2, QSqlRelation('bus', 'BusID', 'BusName'))
        model.setRelation(3, QSqlRelation('bus', 'BusID', 'BusName'))

        # Since this is the QSqlRelationalTableModel, it shows the entire table
        model.setHeaderData(0, Qt.Horizontal, "BranchID")
        model.setHeaderData(1, Qt.Horizontal, "BranchName")
        model.setHeaderData(2, Qt.Horizontal, "FromBus")
        model.setHeaderData(3, Qt.Horizontal, "ToBus")
        model.select()

        # Create View
        view = self.ui.tableView
        view.setModel(model)
        # Hide columns I don't care about
        view.setColumnHidden(4, True)
        view.setColumnHidden(5, True)
        view.setItemDelegate(QSqlRelationalDelegate(view))

        view.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
