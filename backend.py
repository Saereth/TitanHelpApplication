#imports for our libs and deps
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

#Os import for handling file paths
import os

#Initialize the application
app = Flask(__name__)
dbpath = os.path.abspath(os.path.dirname(__file__))

#shutup console
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqllite:///' + os.path.join(dbpath,'titanhelp.db')
 
#Initialize DB 
db = SQLAlchemy(app)

#Initialize Marshmallow
ma = Marshmallow(app)

#create a JsonTicket class for SQL Alchemy to use
#Todo Move logic to JSonTicket.py

class JSONTicket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    description = db.Column(db.String(500))
    date = db.Colummn(db.Integer)

    def __init__(self,name,description,date):
        self.name = name
        self.description = description
        self.date = date

#Define a product schema using marshmallow
class JSONTicketSchema(ma.Schema):
    class Meta:
        fields = ('id','name','description','date')

#Initialize the schema
jsonticket_schema = JSONTicketSchema(strict=True)
jsontickets_schema = JSONTicketSchema(many=True,strict=True)

#Run the microservice
if __name__ == '__main__':
    app.run(debug=True)


