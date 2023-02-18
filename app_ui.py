import os
import shutil
import sys
from PyQt5.QtCore import *
from PyQt5.QtCore import QSize
from PyQt5.QtGui import *
from PyQt5.QtGui import QImage, QPalette, QBrush
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import (
    QVBoxLayout, QWidget, QPushButton )
from PyQt5 import QtCore, QtGui, QtWidgets, QtSql
from PyQt5.QtCore import Qt

import requests
import backend

#from ticket import Ui_ticket_system
#import db_test

"""
Main Application User Interface
"""
class Window(QWidget, QtCore.QAbstractTableModel):
    def __init__(self):
        super(Window, self).__init__()
        # Background image location
        app_path = os.path.abspath(os.path.dirname(__file__))
        oImage = QImage(os.path.join(app_path,'images\\ticket system.png'))
        """ Background Image Sizing | Dimensions Height , Width """
        sImage = oImage.scaled(QSize(800, 600))  # resize Image to widgets size 450, 800
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(sImage))

        """ Window Title Name """
        self.setWindowTitle("Titan Help Application")
        """ Resize Window """
        self.resize(800, 600)#600, 500
        def __init__(self):
            super().__init__()
            self.setLayout(self.layout)

        """   GUI WINDOW || TITLE   """
        # Set up GUI Details
        self.setWindowTitle("Titan Help Application")
        self.setPalette(palette)
        app_path = os.path.abspath(os.path.dirname(__file__))
        icon_file = QIcon(os.path.join(app_path,'images\\atlas.png'))
        self.setWindowIcon(QIcon(icon_file))

        """Create the General page UI."""
        generalTab = QWidget()
        layout = QVBoxLayout()

        """ List box for Displaying Tickets """

        #ticket_list_widget = QListWidget()
        #my_ticket = ticket.curr_tickets
        #my_ticket.append(ticket_system.tickets(self.curr_tickets))
        # function for filling list widget if ticket_list has more than 0 entries


        """   TAB INFORMATION   """
        # Create the tab widget
        tabs = QTabWidget()

        """ List of Tickets """
        # open list of tickets in new paginated window
        def open_current_tickets():
            from ticket import Ui_ticket_system
            #import ticket
            print('Ticket button clicked')
        open_tickets_btn = QPushButton('View Tickets')
        open_tickets_btn.clicked.connect(open_current_tickets)
        layout.addWidget(open_tickets_btn)

        """New ticket button"""
        def create_form_win():
            #from ticket import Ui_ticket_system
            #import ticket
            print('new form clicked')

        new_ticket_btn = QPushButton("Create Ticket")
        new_ticket_btn.clicked.connect(create_form_win)
        layout.addWidget(new_ticket_btn)
        #layout.addWidget(ticket_list_widget)


        """ update ticket """
        refresh_btn = QPushButton("Update Ticket")
        def update_ticket():
            #from ticket import Ui_ticket_system
            import ticket
            #print(Ui_ticket_system.tickets(self.curr_tickets))
        refresh_btn.clicked.connect(update_ticket)
        layout.addWidget(refresh_btn)

        """ Delete ticket """
        delete_btn = QPushButton("Delete Ticket")

        def delete_ticket():
            url = "http://127.0.0.1/tickets/<id>"
            requests.delete(url)

            print('delete ticket started')

        delete_btn.clicked.connect(delete_ticket)
        layout.addWidget(delete_btn)

        """ Tab Layout / Widgets """
        #layout.addWidget(new_ticket_btn)
        layout.setAlignment(Qt.AlignRight)

        """ Database """

        """Display UI"""
        self.show()
        self.setLayout(layout)
#       print(self.children())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())

