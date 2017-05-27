"""
QT Designer wants this class to be in its own file
"""
import sql_example_ui
from PyQt5.QtCore import Qt
from PyQt5 import QtCore
from PyQt5.QtWidgets import (QMainWindow, QApplication, QItemDelegate, QComboBox, QTableView)
from PyQt5 import QtSql
from PyQt5.QtSql import (QSqlQuery, QSqlQueryModel)
import sys
from textwrap import dedent


class MyTableView(QTableView):
    """
    A simple table to demonstrate the QComboBox delegate.
    """
    def __init__(self, *args, **kwargs):
        QTableView.__init__(self, *args, **kwargs)

        # Set the delegate for column 0 of our table
        # self.setItemDelegateForColumn(0, ButtonDelegate(self))
        self.setItemDelegateForColumn(2, ComboDelegate(self))

class ComboDelegate(QItemDelegate):
    """
    A delegate that places a fully functioning QComboBox in every
    cell of the column to which it's applied
    """

    def __init__(self, parent):
        QItemDelegate.__init__(self, parent)

    def createEditor(self, parent, option, index):
        # Different columns will be filled with different queries
        # TODO: Eventually use a completer.
        combo = QComboBox(parent)
        li = []
        li.append(("Bubba", 11))
        li.append(("Gump", 12))
        li.append(("Shrimp", 13))
        li.append(("Grits", 14))
        for s, user_data in li:
            combo.addItem(s, user_data)

        self.currentIndexChanged()
        return combo

    def setEditorData(self, editor, index):
        editor.blockSignals(True)
        editor.setCurrentIndex(int(index.model().data(index)))
        editor.blockSignals(False)

    def setModelData(self, editor, model, index):
        # the model is a subclass of QSqlQueryModel
        #model.setData(index, editor.currentIndex(), role=Qt.EditRole)
        model.setData(index, editor.currentData(), role=Qt.EditRole)

    def currentIndexChanged(self):
        self.commitData.emit(self.sender())