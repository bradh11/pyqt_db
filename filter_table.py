"""
This does a couple cool things building on previous example:
 - Use a nice auto-completing combobox
 - Filter the table view by the value in a combobox

All of this is bound to sql queries
"""
import sql_example_ui
from PyQt5.QtCore import (Qt, QSortFilterProxyModel, QModelIndex)
from PyQt5 import QtCore
from PyQt5.QtGui import (QStandardItem, QStandardItemModel)
from PyQt5.QtWidgets import (QMainWindow, QApplication, QItemDelegate, QComboBox, QTableView, QCompleter, QWidget)
from PyQt5 import QtSql
from PyQt5.QtSql import (QSqlQuery, QSqlQueryModel, QSqlRelationalTableModel, QSqlTableModel, QSqlRelation, QSqlRelationalDelegate)
import sys
from textwrap import dedent


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = sql_example_ui.Ui_MainWindow()
        self.ui.setupUi(self)

        # Setup database
        db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName('example.sqlite')
        db.open() # This is important sometimes
        query = QSqlQuery()
        query.prepare('PRAGMA foreign_keys = ON;')
        query.exec_()

        self.setup_table()
        self.setup_line()

        self.ui.selectLine.currentIndexChanged.connect(self.line_changed)

    def setup_table(self):
        model = QSqlRelationalTableModel()
        # sql = "SELECT branch.BranchID, branch.BranchName, FromBusID, ToBusID FROM branch;"

        view = self.ui.tableView
        view.setModel(model)
        view.show()
        self.refresh_table()

    def refresh_table(self, LineID=None):
        model = self.ui.tableView.model()
        model.setTable('branch')
        model.setEditStrategy(QSqlTableModel.OnFieldChange)
        if LineID is not None:
            model.setFilter('LineID = %s' % LineID)

        # Instead of FromBusID show the BusName
        model.setRelation(2, QSqlRelation('bus', 'BusID', 'BusName'))
        model.setRelation(3, QSqlRelation('bus', 'BusID', 'BusName'))

        # Since this is the QSqlRelationalTableModel, it shows the entire table
        model.setHeaderData(0, Qt.Horizontal, "BranchID")
        model.setHeaderData(1, Qt.Horizontal, "LineID")
        model.setHeaderData(2, Qt.Horizontal, "FromBus")
        model.setHeaderData(3, Qt.Horizontal, "ToBus")
        model.setHeaderData(4, Qt.Horizontal, "ckt")
        model.setHeaderData(5, Qt.Horizontal, "BranchName")
        model.select()


    def setup_line(self):
        """
        Setup the lineSelector Combobox
        """
        mlines = QSqlQueryModel()
        mlines.setQuery("SELECT LineName, LineID FROM line")
        mlines.setHeaderData(0, Qt.Horizontal, "LineID")
        mlines.setHeaderData(1, Qt.Horizontal, "LineName")

        proxy = QSortFilterProxyModel(self)
        proxy.setSourceModel(mlines)

        completer = QCompleter(mlines, proxy)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        completer.setCompletionMode(QCompleter.PopupCompletion)
        completer.setFilterMode(Qt.MatchContains)

        self.ui.selectLine.setEditable(True)
        self.ui.selectLine.setCompleter(completer)
        self.ui.selectLine.setModel(mlines)

    def line_changed(self, row_index):
        model = self.ui.selectLine.model()
        record = model.record(row_index)
        LineID = record.field(1).value()
        self.refresh_table(LineID)
        return

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

            col = 1 # column number of LineID
            row = index.row() # current row number
            LineID = index.model().index(row, col).data()

            sql = dedent("""\
                    SELECT BusName 
                        FROM bus
                    INNER JOIN branch
                        ON branch.FromBusID = bus.BusID
                    INNER JOIN line
                            ON line.LineID = branch.LineID
                    WHERE line.LineID = ?;
                    """)
            # Let any bus associated with the line be selected.
            sql = dedent("""\
                    SELECT bus.BusName 
                    FROM bus
                    INNER JOIN branch
                            ON branch.FromBusID = bus.BusID
                    INNER JOIN line
                            ON line.LineID = branch.LineID
                    WHERE line.LineID = ?
                    UNION
                    SELECT bus.BusName 
                    FROM bus
                    INNER JOIN branch
                            ON branch.ToBusID = bus.BusID
                    INNER JOIN line
                            ON line.LineID = branch.LineID
                    WHERE line.LineID = ?;
                    """)
            query = QSqlQuery()
            #query.prepare('SELECT BusName FROM bus')
            query.prepare(sql)
            query.addBindValue(LineID)
            query.addBindValue(LineID)
            query.exec_()
            while query.next():
                item = QStandardItem(str(query.value(0)))
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
