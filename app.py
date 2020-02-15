import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))
from flask import Flask, g
from flask_restful import Api
from resources.comments import Comments
from utils.db import Sqllite

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False  # show UTF8 characters instead of ASCII in json
api = Api(app)

api.add_resource(Comments, '/api/v1/comments')

def connect_db():
    return Sqllite()

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
