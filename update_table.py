"""
Show a simple table and bind it to the db backend.
"""
import sql_example_ui
from PyQt5 import (QtCore)
from PyQt5.QtWidgets import (QMainWindow, QApplication)
from PyQt5 import QtSql
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = sql_example_ui.Ui_MainWindow()
        self.ui.setupUi(self)

        self.db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName('example.sqlite')

        model = QtSql.QSqlTableModel()
        model.setTable('line')
        model.setEditStrategy(QtSql.QSqlTableModel.OnFieldChange)
        model.select()
        model.setHeaderData(0, QtCore.Qt.Horizontal, "ID")
        model.setHeaderData(1, QtCore.Qt.Horizontal, "LineName")

        view = self.ui.tableView
        view.setModel(model)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())