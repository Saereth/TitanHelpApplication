from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem
from flask import Flask, request, jsonify
from manage_ticket import Ui_TicketWindow
import requests
from backend import app
import math
from PyQt5.QtWidgets import QMessageBox
import json

ENDPOINT = "http://127.0.0.1:5000"
TICKETLIST = ENDPOINT + "/tickets/"
TICKETURL = ENDPOINT + "/ticket"
COUNTURL = ENDPOINT + "/ticket_count"

class Ui_MainWindow(object):#

    #Initialize the class with a default constructor
    def __init__(self):
        super().__init__()

        #setup Ticket manager
        self.total_tickets = self.get_total_tickets()
        self.current_ticket_list = []
        self.ticket_manager = QtWidgets.QMainWindow()
        self.ticket_manager_ui = Ui_TicketWindow(self.ticket_manager)
        self.ticket_manager_ui.setupUi(self.ticket_manager)
        self.ticket_manager.hide()

    def edit_ticket(self):
        if (self.tableWidget.currentRow() == None or self.tableWidget.currentRow() == -1):
            self.alert("Invalid Selection","Please select a valid entry.")
            return

        row = self.tableWidget.currentRow()
        if (self.tableWidget.item(row,0) == None):
            self.alert("Invalid Selection","Please select a valid entry.")
            return
        
        id = self.tableWidget.item(row,0).text()
        url = TICKETURL + "/" + str(id)

        response = requests.get(url).json()
        print("Response: " + json.dumps(response))
        name = response['name']
        description = response['description']
        date = response['date']
        print("Selected ID is:" + id, " Row is: " + str(row), "name is: " + name)       
        self.ticket_manager.show()
        self.ticket_manager_ui.ticket_id.setText(id)
        self.ticket_manager_ui.ticket_name.setText(name)
        self.ticket_manager_ui.ticket_description.setPlainText(description)

    def alert(self,title,message):
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(message)
        x = msg.exec_()
        msg.setIcon(QMessageBox.Critical)

    def new_ticket(self):
        
        self.ticket_manager_ui.ticket_id.clear()
        self.ticket_manager_ui.ticket_name.clear()
        self.ticket_manager_ui.ticket_date.clear()
        self.ticket_manager_ui.ticket_description.clear()
        self.ticket_manager.show()
        self.refresh_ticket_window(False)

    #this checks how many total tickets we have and saves it to the total_tickets variable for pagination maximums in the navigation controls
    def get_total_tickets(self):
        url = COUNTURL
        response = requests.get(url)

        return int(response.json())

    #populate the tableview 
    def populate_ticket_list(self,page=1):
        if page == "" or page == None:
            page = 1
            self.current_page.setText("1")

        if int(page) > math.trunc(self.total_tickets/20)+1:
            page = math.trunc(self.total_tickets/20)+1

        #disable sorting during population, re-eneable after
        self.tableWidget.setSortingEnabled(False)
        self.tableWidget.clear()

        # default to page 1 view if no page is passed - this asks our API to return 20 results starting 
        # at the specified page or starting at the begining if no page is specified

        url = TICKETLIST + str(page)
        print("populate_ticket_list - URL = " + url)
        response = requests.get(url)
        

        #self.current_ticket_list
        jsonResponse = response.json()

        ''' TODO: Add handlers for exceptions/errors. pop up a message box with the error. 
        except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
        except Exception as err:
        print(f'Other error occurred: {err}')
        '''
        tl = self.current_ticket_list
        tl.clear()
        ticket_table = self.tableWidget

        for row, item in enumerate(jsonResponse):
            ticket_table.setItem(row, 0, QTableWidgetItem(str(item['id'])))
            ticket_table.setItem(row, 1, QTableWidgetItem(item['name']))
            ticket_table.setItem(row, 2, QTableWidgetItem(item['date']))
            ticket_table.setItem(row, 3, QTableWidgetItem(item['description']))

        #re-enable sorting after the data has been added to the table, this prevents recursive sorting issue during data load
        self.tableWidget.setSortingEnabled(True)
        
    def delete_ticket(self):
        row = self.tableWidget.currentRow()
        id = self.tableWidget.item(row,0).text()
        print("Selected ID is:" + id, " Row is: " + str(row))

        #TODO: Put in a check to make sure a valid row is selected before passing the id off to the api response
        url = TICKETURL + "/" + id
        print("delete_ticket - URL = " + url)
        response = requests.delete(url)

        #get current page number
        if self.current_page.text() == "":
            self.current_page.setText("1")
            print("set page to 1")

        #update total ticket count
        self.total_tickets = self.get_total_tickets()
        
        #Update ticket list view after delete
        print("Current page: " + self.current_page.text())
        self.populate_ticket_list(self.current_page.text())
    
    def close_windows(self):
        self.ticket_manager.hide()
        MainWindow.close()

    def update_ticket(self):
        id = self.ticket_manager_ui.ticket_id.text()

        if (id == ""):
            self.insert_ticket()
        else:
            name = self.ticket_manager_ui.ticket_name.displayText()
            description = self.ticket_manager_ui.ticket_description.toPlainText()
            date = self.ticket_manager_ui.ticket_date.displayText()
            url = TICKETURL + "/" + str(id)
            ticket_update = {
                "name": f'{name}',
                "description": f'{description}',
                "date": f'{date}'
                            }
            requests.put(url, json=ticket_update)
            self.refresh_ticket_window(True)

    def insert_ticket(self):
            name = self.ticket_manager_ui.ticket_name.displayText()
            description = self.ticket_manager_ui.ticket_description.toPlainText()
            date = self.ticket_manager_ui.ticket_date.displayText()
            url = TICKETURL
            new_ticket_data = {
                "name": f'{name}',
                "description": f'{description}',
                "date": f'{date}'
                            }
            requests.post(url, json=new_ticket_data)
            self.refresh_ticket_window(True)


    def refresh_ticket_window(self,hide=False):
        #update total ticket count
        self.total_tickets = self.get_total_tickets()

        if self.current_page.text() == "":
            self.current_page.setText("1")
        self.populate_ticket_list(self.current_page.text())
        if hide:
            self.ticket_manager.hide()
        else:
            self.ticket_manager.show()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(740, 480)
        MainWindow.setMinimumSize(QtCore.QSize(740, 480))
        MainWindow.setMaximumSize(QtCore.QSize(740, 480))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(15, 66, 111))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(22, 99, 167))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(18, 82, 139))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(7, 33, 55))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(10, 44, 74))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(15, 66, 111))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(7, 33, 55))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ToolTipText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(15, 66, 111))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(22, 99, 167))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(18, 82, 139))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(7, 33, 55))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(10, 44, 74))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(15, 66, 111))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(7, 33, 55))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ToolTipText, brush)
        brush = QtGui.QBrush(QtGui.QColor(7, 33, 55))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(15, 66, 111))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(22, 99, 167))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(18, 82, 139))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(7, 33, 55))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(10, 44, 74))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(7, 33, 55))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(7, 33, 55))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(15, 66, 111))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(15, 66, 111))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(15, 66, 111))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ToolTipText, brush)
        MainWindow.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        MainWindow.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(".\\images/titan-2.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon.addPixmap(QtGui.QPixmap(".\\images/titan-2.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        MainWindow.setWindowIcon(icon)
        MainWindow.setAutoFillBackground(False)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.main_frame = QtWidgets.QFrame(self.centralwidget)
        self.main_frame.setGeometry(QtCore.QRect(9, 9, 711, 451))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(7, 33, 55))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(7, 33, 55))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, brush)
        self.main_frame.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        self.main_frame.setFont(font)
        self.main_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.main_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.main_frame.setObjectName("main_frame")
        self.label = QtWidgets.QLabel(self.main_frame)
        self.label.setGeometry(QtCore.QRect(0, 0, 131, 101))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap(".\\images/titan-2.png"))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.main_frame)
        self.label_2.setGeometry(QtCore.QRect(140, 0, 291, 91))
        font = QtGui.QFont()
        font.setFamily("Modern No. 20")
        font.setPointSize(39)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.tableWidget = QtWidgets.QTableWidget(self.main_frame)
        self.tableWidget.setGeometry(QtCore.QRect(10, 170, 591, 271))
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.NoRole, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.NoRole, brush)
        brush = QtGui.QBrush(QtGui.QColor(7, 33, 55))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(7, 33, 55))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(7, 33, 55))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.NoRole, brush)
        self.tableWidget.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(14)
        self.tableWidget.setFont(font)
        self.tableWidget.setAutoFillBackground(False)
        self.tableWidget.setLineWidth(2)
        self.tableWidget.setAutoScroll(True)
        self.tableWidget.setRowCount(20)
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setObjectName("tableWidget")
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(0, 0, item)
        self.button_previous = QtWidgets.QPushButton(self.main_frame)
        self.button_previous.setGeometry(QtCore.QRect(10, 140, 41, 23))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(7, 33, 55))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(7, 33, 55))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, brush)
        self.button_previous.setPalette(palette)
        self.button_previous.setObjectName("button_previous")
        self.button_next = QtWidgets.QPushButton(self.main_frame)
        self.button_next.setGeometry(QtCore.QRect(100, 140, 41, 23))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(7, 33, 55))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(7, 33, 55))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, brush)
        self.button_next.setPalette(palette)
        self.button_next.setObjectName("button_next")
        self.current_page = QtWidgets.QLineEdit(self.main_frame)
        self.current_page.setGeometry(QtCore.QRect(60, 140, 31, 21))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(7, 33, 55))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        self.current_page.setPalette(palette)
        self.current_page.setText("")
        self.current_page.setMaxLength(3)
        self.current_page.setAlignment(QtCore.Qt.AlignCenter)
        self.current_page.setObjectName("current_page")
        self.button_create_ticket = QtWidgets.QPushButton(self.main_frame)
        self.button_create_ticket.clicked.connect(lambda: self.new_ticket())
        self.ticket_manager_ui.button_confirm_update.clicked.connect(lambda: self.update_ticket())
        self.button_create_ticket.setGeometry(QtCore.QRect(620, 180, 91, 31))
        self.button_create_ticket.setObjectName("button_create_ticket")
        self.button_delete_ticket = QtWidgets.QPushButton(self.main_frame)
        self.button_delete_ticket.setGeometry(QtCore.QRect(620, 260, 91, 31))
        self.button_delete_ticket.setObjectName("button_delete_ticket")
        self.button_delete_ticket.clicked.connect(lambda: self.delete_ticket())
        self.button_update_ticket = QtWidgets.QPushButton(self.main_frame)
        self.button_update_ticket.setGeometry(QtCore.QRect(620, 220, 91, 31))
        self.button_update_ticket.setObjectName("button_update_ticket")
        self.button_update_ticket.clicked.connect(lambda: self.edit_ticket())
        self.button_exit = QtWidgets.QPushButton(self.main_frame)
        self.button_exit.setGeometry(QtCore.QRect(620, 400, 91, 31))
        self.button_exit.setObjectName("button_exit")
        self.button_exit.clicked.connect(self.close_windows)#lambda:QtCore.QCoreApplication.instance().quit())
        self.logo_frame = QtWidgets.QFrame(self.main_frame)
        self.logo_frame.setGeometry(QtCore.QRect(0, 0, 431, 101))
        self.logo_frame.setFrameShape(QtWidgets.QFrame.Box)
        self.logo_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.logo_frame.setObjectName("logo_frame")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Titan Tickets"))
        self.label_2.setText(_translate("MainWindow", "Titan Tickets"))
        self.tableWidget.setSortingEnabled(True)
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "TicketID"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Name"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Date"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "        Description          "))
        __sortingEnabled = self.tableWidget.isSortingEnabled()
        self.tableWidget.setSortingEnabled(False)
        self.tableWidget.setSortingEnabled(__sortingEnabled)
        self.button_previous.setText(_translate("MainWindow", "<<"))

        #decrement current page but idssallow enter a page numer lower than max
        self.button_previous.clicked.connect(lambda: self.current_page.setText(str(max(int(self.current_page.text())-1,1))))
        self.button_next.setText(_translate("MainWindow", ">>"))

        #increment current page but dissallow entering a page number beyond max
        self.button_next.clicked.connect(lambda: self.current_page.setText(str(min(int(self.current_page.text())+1,1+math.trunc(self.total_tickets/20)))))
        self.current_page.setText("1") 
        self.current_page.textChanged.connect(lambda: self.populate_ticket_list(self.current_page.text()))
        self.button_create_ticket.setText(_translate("MainWindow", "Create"))
        self.button_delete_ticket.setText(_translate("MainWindow", "Delete"))
        self.button_update_ticket.setText(_translate("MainWindow", "Edit"))
        self.button_exit.setText(_translate("MainWindow", "Exit"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    ui.populate_ticket_list()
    MainWindow.show()
    sys.exit(app.exec_())
