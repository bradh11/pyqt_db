"""
If the library can be loaded the output looks like this:

    Is Library: True
    can load with QPluginLoader: True
    can load with QLibrary: True

"""
from PyQt5.QtWidgets import QApplication
from PyQt5 import QtCore
from PyQt5.QtSql import QSqlQuery
from PyQt5 import QtSql
import sys
fn = r'C:\Anaconda2\Library\plugins\sqldrivers\qsqlodbc.dll'
#fn = r'C:\Anaconda2\Library\plugins\sqldrivers\qsqlite.dll'
#fn = r'qsqlite.dll'
#fn = r'sqldrivers\qsqlite.dll'
#fn = r'qsqlite.dll'
print "fn: % s" % fn
print "Is Library: %s" % QtCore.QLibrary.isLibrary(fn)
loader = QtCore.QPluginLoader(fn)
print "can load with QPluginLoader: %s" % loader.load()
lib = QtCore.QLibrary(fn)
print "can load with QLibrary: %s" % lib.load()
app = QApplication(sys.argv)
db = QtSql.QSqlDatabase.addDatabase('QODBC')
#db.setHostName('localhost')
s = 'Driver={Microsoft Access Driver (*.mdb, *.accdb)};Dbq=c:\cwebber\pyqt_db\example.accdb;Uid=Admin;Pwd=;'
db.setDatabaseName(s)
db.open()

query = QSqlQuery()
query.prepare('SELECT * FROM bus')
query.exec_()
while query.next():
    print "%s" % query.value(0)

