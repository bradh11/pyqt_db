"""
Show a query in a table view.
"""
import sql_example_ui
from PyQt5 import (QtCore)
from PyQt5.QtWidgets import (QMainWindow, QApplication)
from PyQt5 import QtSql
import sys
from textwrap import dedent

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = sql_example_ui.Ui_MainWindow()
        self.ui.setupUi(self)

        self.db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName('example.sqlite')
        self.db.open() # This is important sometimes

        sql = dedent("""\
                SELECT line.LineID, line.LineName, branch.BranchID, branch.BranchName FROM line
                INNER JOIN branch 
                        ON branch.LineID = line.LineID
                """)

        model = QtSql.QSqlQueryModel()
        model.setQuery(sql)
        model.setHeaderData(0, QtCore.Qt.Horizontal, "LineID")
        model.setHeaderData(1, QtCore.Qt.Horizontal, "LineName")
        model.setHeaderData(2, QtCore.Qt.Horizontal, "BranchID")
        model.setHeaderData(3, QtCore.Qt.Horizontal, "BranchName")

        view = self.ui.tableView
        view.setModel(model)
        view.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())