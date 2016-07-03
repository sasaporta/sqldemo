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
from sqlalchemy.sql import text

app = Flask(__name__)

@app.route('/')
def hello_world():

    # Connect to the database. You'll need to change the connection string.
    engine = create_engine('postgresql://someuser:somepassword@localhost/somedatabasename', echo=True)
    conn = engine.connect()

    # Query the database. You'll need to change the query.
    # Format the results as a JSON dictionary.
    records = conn.execute('select id, name from public.user where id < 10').fetchall()
    results = {'users': []}
    for record in records:
        results['users'].append({'id': record.id, 'name': record.name})

    # Return a JSON response. Use a header (CORS) to allow access from a
    # different domain.
    response = make_response(jsonify(**results))
    origin = request.headers['Origin']
    response.headers['Access-Control-Allow-Origin'] = origin

    return response

if __name__ == '__main__':
    app.run(debug=True)
