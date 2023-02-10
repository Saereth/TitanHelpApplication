"""
This class is responsible for creating, retrieving and deleting tickets
When clicked the application layer should create an Instance of a Ticket object
and store the Ticket in a database
"""

"""
1: Create new ticket option to be placed within ticket list.
    Initilized as an empty list
"""
ticket = []
curr_tickets = []
class ticket_system():

    def __init__(self):
        self.ticket = ticket
        self.curr_tickets = curr_tickets

    def tickets(self):
        curr_tickets = ticket
        print('current tickets: ', curr_tickets)

    def create_ticket(self):
        print('Titan Ticket Wizard Starting up!')
        #print('Enter new ticket name')
        new_ticket = input('Enter new ticket name')

        new_ticket
        ticket.append(new_ticket)
        print(ticket)

ticket_system()