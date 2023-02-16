from os.path import exists
from PyQt6.QtWidgets import *
from PyQt6.QtSql import *
# https://github.com/pyqt/examples/tree/_/src/15%20PyQt%20database%20example

import sys

if not exists("patients.db"):
    print("File projects.db does not exist. Please run initdb.py.")
    sys.exit()

app = QApplication([])
db = QSqlDatabase.addDatabase("QSQLITE")
db.setDatabaseName("patients.db")
db.open()
model = QSqlTableModel(None, db)
model.setTable("patients")
model.select()
view = QTableView()
view.setModel(model)
#view.show()
#app.exec()