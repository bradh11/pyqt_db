"""
This continues the filter_table.py example and adds comboboxes to edit
some of the fields

Somewhat complex view of a query with some filters.
This example also allows editing of some data in the table.

We should be able to edit:
  - FromBus, ToBus, BranchID

Values should be restricted to values currently associated with the Line.

Also add copy/delete rows.  (Maybe make new rows a different color?)
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

BUS_LIST = dedent("""\
        SELECT bus.BusName, bus.BusID 
        FROM bus
        INNER JOIN branch
                ON branch.FromBusID = bus.BusID
        INNER JOIN line
                ON line.LineID = branch.LineID
        WHERE line.LineID = ?
        UNION
        SELECT bus.BusName, bus.BusID 
        FROM bus
        INNER JOIN branch
                ON branch.ToBusID = bus.BusID
        INNER JOIN line
                ON line.LineID = branch.LineID
        WHERE line.LineID = ?;
        """)

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
        #self.setup_branch_filter()
        #self.setup_bus_filter()

        self.ui.filterBus.setEditable(False)
        self.ui.filterBranch.setEditable(False)
        self.ui.tableView.setSortingEnabled(True)

        # Update comboboxes the first time without events.
        # Ideally everything is just kept in-sync without events (using proxies maybe?)
        self.ui.selectLine.setCurrentIndex(-1)
        self.ui.selectLine.currentIndexChanged.connect(self.line_changed)
        self.ui.selectLine.activated.connect(self.reset_filters)
        self.ui.selectLine.currentIndexChanged.connect(self.refresh_table)
        self.ui.filterBranch.currentIndexChanged.connect(self.refresh_table)
        self.ui.filterBus.currentIndexChanged.connect(self.refresh_table)
        self.ui.copyButton.clicked.connect(self.copy_row)
        self.ui.deleteButton.clicked.connect(self.delete_row)

    def copy_row(self):
        # Which row is selected
        idxs = self.ui.tableView.selectionModel().selectedRows()
        if len(idxs) != 1:
            return
        else:
            index = idxs[0]
        BranchID = self.ui.tableView.model().data(index)

        # Get selected BranchID
        sql = dedent("""\
            INSERT INTO branch (BranchID, LineID, FromBusID, ToBusID, ckt, BranchName) 
            SELECT NULL, LineID, FromBusID, ToBusID, ckt, BranchName
            FROM branch
            WHERE BranchID = ?;
            """)
        query = QSqlQuery()
        query.prepare(sql)
        query.addBindValue(BranchID)
        query.exec_()
        self.refresh_table()
        return

    def delete_row(self):
        idxs = self.ui.tableView.selectionModel().selectedRows()
        if len(idxs) != 1:
            return
        else:
            index = idxs[0]
        BranchID = self.ui.tableView.model().data(index)
        sql = "DELETE FROM branch WHERE BranchID = ?"
        query = QSqlQuery()
        query.prepare(sql)
        query.addBindValue(BranchID)
        query.exec_()
        self.refresh_table()
        return

    def reset_filters(self):
        self.ui.filterBranch.setCurrentIndex(-1)
        self.ui.filterBus.setCurrentIndex(-1)
        self.ui.filterEquipment.setText('')

    def setup_table(self):
        # We have to subclass this model for advanced functions like disable editing
        # on some rows/columns.
        model = QSqlRelationalTableModel()
        model.setTable('branch')
        model.setEditStrategy(QSqlTableModel.OnFieldChange)
        model.setRelation(2, QSqlRelation('bus', 'BusID', 'BusName')) # FromBus
        model.setRelation(3, QSqlRelation('bus', 'BusID', 'BusName')) # ToBus
        model.select()

        # sql = "SELECT branch.BranchID, branch.BranchName, FromBusID, ToBusID FROM branch;"

        view = self.ui.tableView
        view.setModel(model)
        view.setItemDelegate(QSqlRelationalDelegate(view))
        view.show()
        self.refresh_table()

    def refresh_table(self):
        tmodel = self.ui.tableView.model()

        index = self.ui.filterBranch.currentIndex()
        if index > -1:
            model = self.ui.filterBranch.model()
            record = model.record(index)
            BranchID = record.field(1).value()
        else:
            BranchID = None

        index = self.ui.selectLine.currentIndex()
        if index > -1:
            record = self.ui.selectLine.model().record(index)
            LineID = record.field(1).value()
        else:
            LineID = None

        index = self.ui.filterBus.currentIndex()
        if index > -1:
            record = self.ui.filterBus.model().record(index)
            BusID = record.field(1).value()
        else:
            BusID = None
        equipment_alpha = self.ui.filterEquipment.text()

        # setFilter() only accepts one filter string.
        filters = []
        if LineID is not None:
            filters.append('LineID = %s' % LineID)
        else:
            filters.append('LineID IS NULL')
        if BranchID is not None:
            filters.append('BranchID = %s' % BranchID)
        if BusID is not None:
            filters.append('(FromBusID = %s OR ToBusID = %s)' % (BusID, BusID))
        if len(filters) > 0:
            filter = " AND ".join(filters)
            tmodel.setFilter(filter)

        # Instead of FromBusID show the BusName
        tmodel.setRelation(2, QSqlRelation('bus', 'BusID', 'BusName'))
        tmodel.setRelation(3, QSqlRelation('bus', 'BusID', 'BusName'))

        # Since this is the QSqlRelationalTableModel, it shows the entire table
        tmodel.setHeaderData(0, Qt.Horizontal, "BranchID")
        tmodel.setHeaderData(1, Qt.Horizontal, "LineID")
        tmodel.setHeaderData(2, Qt.Horizontal, "FromBus")
        tmodel.setHeaderData(3, Qt.Horizontal, "ToBus")
        tmodel.setHeaderData(4, Qt.Horizontal, "ckt")
        tmodel.setHeaderData(5, Qt.Horizontal, "BranchName")
        tmodel.select()

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

    def get_LineID(self):
        index = self.ui.selectLine.currentIndex()
        if index > -1:
            record = self.ui.selectLine.model().record(index)
            LineID = record.field(1).value()
        else:
            LineID = None
        return LineID

    def setup_branch_filter(self, LineID=None):
        """
        Setup the lineSelector Combobox
        """
        mbranches = QSqlQueryModel()

        LineID = self.get_LineID()
        if LineID is not None:
            query = QSqlQuery()
            query.prepare("SELECT BranchName, BranchID, LineID FROM branch WHERE LineID=?")
            query.addBindValue(LineID)
            query.exec_()
        else:
            query = ''
        mbranches.setQuery(query)
        mbranches.setHeaderData(0, QtCore.Qt.Horizontal, 'BranchName')
        mbranches.setHeaderData(1, QtCore.Qt.Horizontal, 'BranchID')
        self.ui.filterBranch.setModel(mbranches)
        self.ui.filterBranch.show()

    def setup_bus_filter(self, LineID=None):
        """
        Setup the lineSelector Combobox
        """
        LineID = self.get_LineID()
        if LineID is not None:
            query = QSqlQuery()
            query.prepare(BUS_LIST)
            query.addBindValue(LineID)
            query.addBindValue(LineID)
            query.exec_()
        else:
            query = None
        mbus = QSqlQueryModel()
        mbus.setQuery(query)
        mbus.setHeaderData(0, QtCore.Qt.Horizontal, 'BusID')
        mbus.setHeaderData(1, QtCore.Qt.Horizontal, 'BusName')
        self.ui.filterBus.setModel(mbus)
        self.ui.filterBus.show()

    def line_changed(self):
        self.setup_branch_filter()
        self.setup_bus_filter()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
