import sqlite3
connection = sqlite3.connect("patients.db")
cursor = connection.cursor()
cursor.execute("""
    CREATE TABLE patients
    (lastname TEXT, firstname TEXT, phonenumber INTEGER)
""")
cursor.execute("""INSERT INTO patients VALUES 
    ('Crawford', 'Alex', 111-111-1111),
    ('Craw', 'Alex', 111-111-1111),
    ('Ford', 'Alex', 111-111-1111)
""")
connection.commit()