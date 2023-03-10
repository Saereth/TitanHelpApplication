from PyQt5 import QtCore, QtGui, QtWidgets
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow import Schema, fields
import json
import jsonschema
from jsonschema import validate
#Os import for handling file paths
import os
import requests

# Initialize the application
app = Flask(__name__)
dbpath = os.path.abspath(os.path.dirname(__file__))

# shutup console
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(dbpath, 'titanhelp.db')

url = "http://localhost:5000/ticket"

ENDPOINT = "http://127.0.0.1:5000"
TICKETLIST = ENDPOINT + "/tickets/"
TICKETURL = ENDPOINT + "/ticket"
COUNTURL = ENDPOINT + "/ticket_count"

db = SQLAlchemy(app)
ticketSchema = {
    'type': 'object',
    'properties': {
    'id': {'type': 'number'},
    'name':{'type': 'string', 'minLength':1, 'maxLength':25},
    'date': {'type': 'number', 'minLength':8, 'maxLength': 8},
    'description':{'type': 'string', 'minLength':1, 'maxLength':25}
    }
}
class Ui_TicketWindow(object):

    def __init__(self,parent):
        super().__init__()
        self.parent = parent

    def setupUi(self, TicketWindow):
        TicketWindow.setObjectName("TicketWindow")
        TicketWindow.resize(610, 337)
        TicketWindow.setMinimumSize(QtCore.QSize(610, 337))
        TicketWindow.setMaximumSize(QtCore.QSize(610, 337))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(15, 66, 111))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(15, 66, 111))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(15, 66, 111))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(15, 66, 111))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(15, 66, 111))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(15, 66, 111))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(15, 66, 111))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        TicketWindow.setPalette(palette)
        TicketWindow.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(".\\images/titan-2.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        TicketWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(TicketWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label_name = QtWidgets.QLabel(self.centralwidget)
        self.label_name.setGeometry(QtCore.QRect(60, 60, 61, 21))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        self.label_name.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily("Modern No. 20")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_name.setFont(font)
        self.label_name.setObjectName("label_name")
        self.label_name_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_name_2.setGeometry(QtCore.QRect(70, 100, 51, 21))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        self.label_name_2.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily("Modern No. 20")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_name_2.setFont(font)
        self.label_name_2.setObjectName("label_name_2")
        self.label_name_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_name_3.setGeometry(QtCore.QRect(30, 20, 91, 21))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        self.label_name_3.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily("Modern No. 20")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_name_3.setFont(font)
        self.label_name_3.setObjectName("label_name_3")
        self.label_name_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_name_4.setGeometry(QtCore.QRect(10, 140, 111, 21))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        self.label_name_4.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily("Modern No. 20")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_name_4.setFont(font)
        self.label_name_4.setObjectName("label_name_4")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(130, 20, 481, 261))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.ticket_id = QtWidgets.QLabel(self.frame)
        self.ticket_id.setGeometry(QtCore.QRect(10, 0, 41, 21))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(160, 160, 160))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(157, 157, 157))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(143, 143, 143))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(140, 140, 140))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(160, 160, 160))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(160, 160, 160))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(157, 157, 157))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(143, 143, 143))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(140, 140, 140))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(160, 160, 160))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(160, 160, 160))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(143, 143, 143))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        """ Ticket ID """
        self.ticket_id.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.ticket_id.setFont(font)
        self.ticket_id.setAutoFillBackground(True)
        self.ticket_id.setFrameShape(QtWidgets.QFrame.Box)
        self.ticket_id.setFrameShadow(QtWidgets.QFrame.Plain)
        self.ticket_id.setText("")
        self.ticket_id.setTextFormat(QtCore.Qt.PlainText)
        self.ticket_id.setAlignment(QtCore.Qt.AlignCenter)
        self.ticket_id.setTextInteractionFlags(QtCore.Qt.NoTextInteraction) # set to allow input
        self.ticket_id.setObjectName("ticket_id")
        """ Ticket Name """
        self.ticket_name = QtWidgets.QLineEdit(self.frame)
        self.ticket_name.setGeometry(QtCore.QRect(10, 40, 171, 21))
        self.ticket_name.setObjectName("ticket_name")
        """ Ticket Date """
        self.ticket_date = QtWidgets.QLineEdit(self.frame)
        self.ticket_date.setGeometry(QtCore.QRect(10, 80, 71, 21))
        self.ticket_date.setText("")
        self.ticket_date.setMaxLength(10)
        self.ticket_date.setObjectName("ticket_date")
        """ Ticket Description """
        self.ticket_description = QtWidgets.QPlainTextEdit(self.frame)
        self.ticket_description.setGeometry(QtCore.QRect(10, 120, 441, 131))
        self.ticket_description.setPlainText("")
        self.ticket_description.setObjectName("ticket_description")

        """ Confirm Ticket Button """
        self.button_confirm_update = QtWidgets.QPushButton(self.centralwidget)
        self.button_confirm_update.setGeometry(QtCore.QRect(420, 300, 75, 23))
        self.button_confirm_update.setObjectName("button_confirm_update")
        # define function to insert new information into titanticket.py QTableWidget
        self.button_confirm_update.clicked.connect(lambda:self.confirm_choice)

        """ Cancel Ticket Button """
        self.button_cancel = QtWidgets.QPushButton(self.centralwidget)
        self.button_cancel.setGeometry(QtCore.QRect(510, 300, 75, 23))
        self.button_cancel.clicked.connect(lambda:self.parent.hide())
        self.button_cancel.setObjectName("button_cancel")
        TicketWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(TicketWindow)
        QtCore.QMetaObject.connectSlotsByName(TicketWindow)

    def retranslateUi(self, TicketWindow):
        _translate = QtCore.QCoreApplication.translate
        TicketWindow.setWindowTitle(_translate("TicketWindow", "Titan Tickets - Manage Ticket"))
        self.label_name.setText(_translate("TicketWindow", "Name"))
        self.label_name_2.setText(_translate("TicketWindow", "Date"))
        self.label_name_3.setText(_translate("TicketWindow", "TicketID"))
        self.label_name_4.setText(_translate("TicketWindow", "Description"))
        self.button_confirm_update.setText(_translate("TicketWindow", "Confirm"))
        self.button_cancel.setText(_translate("TicketWindow", "Cancel"))
    
    def create_new_ticket(self):
        new_ticket = {
            "name": f'{self.ticket_name.displayText()}',
            "description": f'{self.ticket_description.toPlainText()}',
            "date": f'{self.ticket_date.displayText()}'
                        }
        response = requests.post(url, json=new_ticket)
        
        return response

    def update_ticket(self):
        pass

    def confirm_choice(self, type="Insert"):
        #import titanticket
        #titan = titanticket.Ui_TicketWindow.setupUi
        if type == "Insert":
            print('validating data')
            id = self.ticket_manager_ui.ticket_id.text()
            name = self.ticket_manager_ui.ticket_name.text()
            description = self.ticket_description.toPlainText()
            date = self.ticket_manager_ui.ticket_date.displayText()
            ENDPOINT = "http://127.0.0.1:5000"
            TICKETURL = ENDPOINT + "/ticket"
            url = TICKETURL + "/" + str(id)
            ticket_update = {
                "name": f'{name}',
                "description": f'{description}',
                "date": f'{date}'
                        }
            print('validating data started')
            validate(instance={id, name, description, date}, schema=ticketSchema)
            print('validating data finished')
            self.validateJson(ticket_update)
            self.check_validity(self,ticketSchema)
            requests.put(url, json=ticket_update)
            self.refresh_ticket_window(True)
            
    def validateJson(jsonData):
        try:
            validate(instance=jsonData, schema=ticketSchema)
            print('validated')
        except jsonschema.exceptions.ValidationError as err:
            return False
        return True
    
    def check_validity(self,jsonData):
        isValid = self.validateJson(jsonData)
        if isValid:
            print(jsonData)
            print('Provided JSON data is Valid')
        else:
            print(jsonData)
            print('Given JSON data is invalid')



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    TicketWindow = QtWidgets.QMainWindow()
    ui = Ui_TicketWindow(object)
    ui.setupUi(TicketWindow)
    TicketWindow.show()
    sys.exit(app.exec_())
