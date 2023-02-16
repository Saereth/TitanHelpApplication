"""
This class is responsible for creating, retrieving and deleting tickets
When clicked the application layer should create an Instance of a Ticket object
and store the Ticket in a database
"""
import flask
import sys
import sqlite3
from PyQt5.QtWidgets import QDialogButtonBox, QLineEdit, QComboBox, QSpinBox, QGroupBox, QVBoxLayout, QDialog, \
    QApplication, QLabel, QFormLayout
from PyQt5 import QtCore, QtGui, QtWidgets, QtSql

"""
1: Create new ticket option to be placed within ticket list.
    Initilized as an empty lis
"""
class Ui_ticket_system(object):
    """ Display new Window for list of tickets paginated """
    def setupUi(self, ticket_system):
        ticket_system.setObjectName('Ticket Database')
        ticket_system.resize(1000, 800)
        ticket_system.setMinimumSize(QtCore.QSize(1000, 800))

        self.centralWidget = QtWidgets.QWidget(ticket_system)
        self.centralWidget.setObjectName("Central")
        self.frame = QtWidgets.QFrame(self.centralWidget)
        self.frame.setGeometry(QtCore.QRect(0, 0, 1000, 800))

        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("Frame")

        """ Output table """
        self.tableWidget = QtWidgets.QTableWidget(self.frame)
        self.tableWidget.setGeometry(QtCore.QRect(0, 0, 1000, 800))
        self.tableWidget.setRowCount(20)
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setObjectName("Table")

        """ initialize items for table """
        id_item = QtWidgets.QTableWidgetItem() # id
        name_item = QtWidgets.QTableWidgetItem() # name
        desc_item = QtWidgets.QTableWidgetItem() # description
        date_item = QtWidgets.QTableWidgetItem() # date

        # Insertion of above items into table
        self.tableWidget.setHorizontalHeaderItem(0, id_item)
        self.tableWidget.setHorizontalHeaderItem(1, name_item)
        self.tableWidget.setHorizontalHeaderItem(2, desc_item)
        self.tableWidget.setHorizontalHeaderItem(3, date_item)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(200)
        #self.tableWidget.verticalHeader().setMinimumSize(50)
        ticket_system.setCentralWidget(self.centralWidget)

        self.retranslateUi(ticket_system)
        QtCore.QMetaObject.connectSlotsByName(ticket_system)

        """ Connect to titanhelp.db """
        connect = sqlite3.connect('titanhelp.db')

    def retranslateUi(self, ticket_system):
        _translate = QtCore.QCoreApplication.translate
        ticket_system.setWindowTitle(_translate("Ticket Window", "List of Available tickets"))
        self.tableWidget.horizontalHeaderItem(0)
        id_item = self.tableWidget.horizontalHeaderItem(0)
        id_item.setText(_translate("Ticket Window", "ID"))
        name_item = self.tableWidget.horizontalHeaderItem(1)
        name_item.setText(_translate('Ticket Window', 'Name'))
        desc_item = self.tableWidget.horizontalHeaderItem(2)
        desc_item.setText(_translate('Ticket Window', 'Description'))
        date_item = self.tableWidget.horizontalHeaderItem(3)
        date_item.setText(_translate('Ticket Window', 'Date'))

    """ Name of ticket """

    """ Navigation """

    """ Page number """

    print('ticket form')

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ticket_system = QtWidgets.QMainWindow()
    ui = Ui_ticket_system()
    ui.setupUi(ticket_system)
    ticket_system.show()
    sys.exit(app.exec_())