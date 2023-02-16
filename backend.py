#imports for our libs and deps
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow import Schema, fields

#Os import for handling file paths
import os

#Initialize the application
app = Flask(__name__)
dbpath = os.path.abspath(os.path.dirname(__file__))

#shutup console
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(dbpath,'titanhelp.db')
 
#Initialize DB 
db = SQLAlchemy(app)

#Initialize Marshmallow
ma = Marshmallow(app)

#create a JsonTicket class for SQL Alchemy to use
#Todo Move logic to JSonTicket.py

class JSONTicket(db.Model):
    __tablename__ = 'tickets'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    description = db.Column(db.String())
    date = db.Column(db.String())

    def __init__(self,name,description,date):
        self.name = name
        self.description = description
        self.date = date

#Define a product schema using marshmallow
class JSONTicketSchema(ma.Schema):
    class Meta:
        fields = ('id','name','description','date')

#Initialize the schema
jsonticket_schema = JSONTicketSchema()
jsontickets_schema = JSONTicketSchema(many=True)

#Define App Routes for basic CRUD

#Create Ticket
@app.route('/ticket', methods=['POST'])
def add_ticket():
    name = request.json['name']
    description = request.json['description']
    date = request.json['date']

    new_jsonticket = JSONTicket(name,description,date)
    db.session.add(new_jsonticket)
    db.session.commit()
    return jsonify(jsonticket_schema.dump(new_jsonticket))

# Get Tickets without pagenumber
@app.route('/tickets', methods=['GET'])
def get_tickets_pageless():
    ticket_list = JSONTicket.query.paginate(page=1,per_page=20)
    result = jsontickets_schema.dump(ticket_list)
    return jsonify(result)

# Get Tickets with pagenumber
@app.route('/tickets/<page_num>', methods=['GET'])
def get_tickets(page_num):
    ticket_list = JSONTicket.query.paginate(page=int(page_num),per_page=20)
    result = jsontickets_schema.dump(ticket_list)
    return jsonify(result)

# Get Single Ticket
@app.route('/ticket/<id>', methods=['GET'])
def get_ticket(id):
    ticket = JSONTicket.query.get(id)
    return jsonticket_schema.jsonify(ticket)

#Update Ticket
@app.route('/ticket/<id>', methods=['PUT'])
def update_ticket(id):
    ticket = JSONTicket.query.get(id)
    name = request.json['name']
    description = request.json['description']
    date = request.json['date']

    ticket.name = name
    ticket.description = description
    ticket.date = date
    db.session.commit()  
    
    return jsonify(jsonticket_schema.dump(ticket))

#Delete Ticket
@app.route('/ticket/<id>', methods=['DELETE'])
def delete_ticket(id):
    ticket = JSONTicket.query.get(id)
    db.session.delete(ticket)
    db.session.commit()
    
    return jsonticket_schema.jsonify(ticket)

#Run the microservice
if __name__ == '__main__':
    app.run(debug=True)


