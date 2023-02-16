import sys

from PyQt5.QtCore import Qt
from PyQt5.QtSql import  QSqlDatabase, QSqlTableModel
from PyQt5.QtWidgets import ( QApplication, QMainWindow, QMessageBox, QTableView)

class Contacts(QMainWindow):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.setWindowTitle("QTableView Example")
        self.resize(415, 200)

        self.model = QSqlTableModel(self)
        self.model.setTable('contacts')
        self.model.setEditStrategy(QSqlTableModel.OnFieldChange)
        self.model.setHeaderData(0, Qt.Horizontal, "ID")
        self.model.select()
        """ Create View """
        self.view = QTableView()
        self.view.setModel(self.model)
        self.view.resizeColumnToContents(self, 1)
        self.setCentralWidget(self.view)

def createConnection():
    con = QSqlDatabase.addDatabase('QSQLITE')
    con.setDatabaseName('contacts.sqlite')
    if not con.open():
        QMessageBox.critical(
                None,
                "QTableView - Error!",
              "Database Error: %s" % con.lastError().databaseText()
            )
        return False
    return True

app = QApplication(sys.argv)
if not createConnection():
    sys.exit(1)
win = Contacts()
win.show()
sys.exit(app.exec_())