from flask import Flask, jsonify, make_response, request
import json
from sqlalchemy import create_engine
from sqlalchemy.sql import text

app = Flask(__name__)

@app.route('/')
def hello_world():
    engine = create_engine('postgresql://master:jJKty7j7yhHH67uy@localhost/suitedev', echo=True)
    conn = engine.connect()
    records = conn.execute('select id, name from public.user where id < 10').fetchall()
    results = {'users': []}
    for record in records:
        results['users'].append({'id': record.id, 'name': record.name})

    response = make_response(jsonify(**results))
    origin = request.headers['Origin']
    response.headers['Access-Control-Allow-Origin'] = origin

    return response

if __name__ == '__main__':
    app.run(debug=True)
