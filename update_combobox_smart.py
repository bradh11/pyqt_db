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
        #model.setHeaderData(1, Qt.Horizontal, "LineID")
        model.setHeaderData(2, Qt.Horizontal, "FromBus")
        model.setHeaderData(3, Qt.Horizontal, "ToBus")
        model.setHeaderData(4, Qt.Horizontal, "ckt")
        model.setHeaderData(5, Qt.Horizontal, "BranchName")
        model.select()

        # Create View
        view = self.ui.tableView
        view.setModel(model)
        # Hide columns I don't care about
        view.setColumnHidden(1, True)
        view.setItemDelegate(MyDelegate(view))

        view.show()


class MyDelegate(QSqlRelationalDelegate):
    def __init__(self, parent=None):
        super(MyDelegate, self).__init__()

    def createEditor(self, parent, option, index):
        """
        Create combobox based on which branch is selected.  This is a result of a query,
        but I'm not sure the best way to run the query.
        """
        if index.column() in (2,3):
            combo = QComboBox(parent)
            model = combo.model()
            item = QStandardItem('Bubba')
            model.appendRow(item)
            item = QStandardItem('Gump')
            model.appendRow(item)
            item = QStandardItem('Shrimp')
            model.appendRow(item)
            item = QStandardItem('Grits')
            model.appendRow(item)
            combo.setModel(model)
            return combo
        else:
            # For every other column use the normal method
            return super(MyDelegate, self).createEditor(parent, option, index)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
