import os
import shutil
import sys

import self
from PyQt5.QtCore import *
from PyQt5.QtCore import QSize
from PyQt5.QtGui import *
from PyQt5.QtGui import QImage, QPalette, QBrush
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import (
    QVBoxLayout, QWidget, QPushButton, )

import ticket


class Window(QWidget):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        # Background image location
        oImage = QImage("E:\School\CEN4031.Adv Program Development Framework\TitanHelpApplication\images\\ticket system.png")
        """ Background Image Sizing | Dimensions Height , Width """
        sImage = oImage.scaled(QSize(800, 600))  # resize Image to widgets size 450, 800
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(sImage))
        self.curr_tickets = ticket.curr_tickets
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
        self.setWindowIcon(QIcon("E:\School\CEN4031.Adv Program Development Framework\TitanHelpApplication\images\\atlas.png"))

        """Create the General page UI."""
        generalTab = QWidget()
        layout = QVBoxLayout()

        """ List box for Displaying Tickets """
        from ticket import ticket_system
        ticket_list_widget = QListWidget()
        my_ticket = ticket.curr_tickets
        my_ticket.append(ticket_system.tickets(self.curr_tickets))
        # function for filling list widget if ticket_list has more than 0 entries


        """   TAB INFORMATION   """
        # Create the tab widget
        tabs = QTabWidget()

        """New ticket button"""
        new_ticket_btn = QPushButton("Create New Ticket")
        new_ticket_btn.clicked.connect(ticket.ticket_system.create_ticket)
        layout.addWidget(new_ticket_btn)
        layout.addWidget(ticket_list_widget)

        """refresh list"""
        refresh_btn = QPushButton("Refresh List")
        def refresh():
            print(ticket_system.tickets(self.curr_tickets))
            if len(my_ticket) != 0:
                ticket_list_widget.addItems(ticket_system.tickets(self.curr_tickets))
                print(my_ticket, "added to list widget")
        refresh_btn.clicked.connect(refresh)
        layout.addWidget(refresh_btn)


        """ Tab Layout / Widgets """
        #layout.addWidget(new_ticket_btn)
        layout.setAlignment(Qt.AlignRight)

        # tab Close Window Button
        generalTab.closeButton = QPushButton(generalTab)
        generalTab.closeButton.setText("Close")  # text
        generalTab.closeButton.setIcon(QIcon("close.png"))  # icon
        generalTab.closeButton.setShortcut('Ctrl+D')  # shortcut key
        generalTab.closeButton.clicked.connect(self.close)
        generalTab.closeButton.setToolTip("Close the widget")  # Tool tip
        generalTab.closeButton.move(10, 150)
        generalTab.setLayout(layout)
        #return generalTab

        """Display UI"""
        self.show()
        self.setLayout(layout)
        print(self.children())







if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
