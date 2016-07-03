"""
Example of a Python Flask route that retrieves data from a SQL database and
returns the results as a JSON dictionary.

A Flask tutorial: http://flask.pocoo.org/docs/0.11/tutorial/
Another Flask tutorial: http://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world
Part of the SQLAlchemy documentation: http://docs.sqlalchemy.org/en/latest/core/tutorial.html
"""

from flask import Flask, jsonify, make_response, request
import json
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData
from sqlalchemy.sql import text

app = Flask(__name__)

@app.route('/')
def hello_world():

    # Connect to the database and create some test data.
    metadata = MetaData()
    users = Table('users', metadata,
        Column('id', Integer, primary_key=True),
        Column('name', String),
        Column('fullname', String),
    )
    engine = create_engine('sqlite:///:memory:', echo=True)
    conn = engine.connect()
    metadata.create_all(engine)
    ins = users.insert().values(name='jack', fullname='Jack Jones')
    result = conn.execute(ins)
    ins = users.insert().values(name='joe', fullname='Joe Schmo')
    result = conn.execute(ins)

    # Query the database. Format the results as a JSON dictionary.
    records = conn.execute('select id, name from users').fetchall()
    print 'records =', records
    results = {'users': []}
    for record in records:
        print 'record =', record
        results['users'].append({'id': record.id, 'name': record.name})

    # Return a JSON response. Use a header (CORS) to allow access from a
    # different domain.
    response = make_response(jsonify(**results))
    origin = request.headers['Origin']
    response.headers['Access-Control-Allow-Origin'] = origin

    return response

if __name__ == '__main__':
    app.run(debug=True)
