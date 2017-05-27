"""
Super simple combobox and completer
"""
from PyQt5.QtCore import (Qt, QSortFilterProxyModel)
from PyQt5 import QtCore
from PyQt5.QtGui import (QStandardItem, QStandardItemModel)
from PyQt5.QtWidgets import (QMainWindow, QApplication, QItemDelegate, QComboBox, QTableView, QCompleter, QWidget, QVBoxLayout)
from PyQt5 import QtSql
from PyQt5.QtSql import (QSqlQuery, QSqlQueryModel, QSqlRelationalTableModel, QSqlTableModel, QSqlRelation, QSqlRelationalDelegate)
import sys
from textwrap import dedent


class FilteringComboBox(QComboBox):
    def __init__(self, parent=None, **kwargs):
        QComboBox.__init__(self, parent)
        self.setEditable(True)
        self._proxy = QSortFilterProxyModel(self)
        self._proxy.setSourceModel(self.model())

        self._completer = QCompleter(self._proxy, self)
        self._completer.setCaseSensitivity(Qt.CaseInsensitive)
        self._completer.setCompletionMode(QCompleter.PopupCompletion)
        self._completer.setFilterMode(Qt.MatchContains)
        self.setCompleter(self._completer)


if __name__ == "__main__":
    from sys import argv, exit


    class Widget(QWidget):
        def __init__(self, parent=None, **kwargs):
            QWidget.__init__(self, parent, **kwargs)

            cb = FilteringComboBox(self)
            cb.addItems(['Item {0}'.format(i) for i in xrange(100)])
            QVBoxLayout(self).addWidget(cb)


    a = QApplication(argv)
    w = Widget()
    w.show()
    w.raise_()
    exit(a.exec_())
