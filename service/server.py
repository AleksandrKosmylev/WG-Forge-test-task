import json
import os
from dotenv import load_dotenv
from flask import request
from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import psycopg2
import db

load_dotenv()
app = Flask(__name__)
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["600 per minute"],
    storage_uri="memory://"
)

app.config['DATABASE_URL'] = os.getenv('DATABASE_URL')
app.config.update(
    SECRET_KEY=os.getenv('SECRET_KEY')
)


def get_db():
    return psycopg2.connect(app.config['DATABASE_URL'])


@app.errorhandler(429)
def ratelimit_handler(e):
    return "429 Too Many Requests"


@app.route('/')
def welcome():
    return 'Welcome to cats database'


@app.route("/ping")
def ping():
    return "Cats Service. Version 0.1"


@app.route("/cats", methods=['GET'])
def show_cats():
    error = None
    attributes = request.values
    if attributes and attributes != '':
        list_of_cats = db.get_db_data_cats(get_db)
        data = json.loads(list_of_cats)
        table_keys = list(data[0])
        len_of_list = len(data)
        if "attribute" in attributes:
            if attributes['attribute'] in table_keys:
                if attributes['order'] == 'asc':
                    data = sorted(data, key=lambda d: d[attributes['attribute']], reverse=False)
                elif attributes['order'] == 'desc':
                    data = sorted(data, key=lambda d: d[attributes['attribute']], reverse=True)
                else:
                    error = " Order attribute is incorrect"
                    return error
            else:
                error = "Attribute is incorrect"
                return error
        if "offset" in attributes:
            offset = int(attributes["offset"])
            if offset >= len_of_list:
                error = " Check offset value. Value is too big"
                return error
            else:
                if 'limit' in attributes:
                    limit = int(attributes['limit'])
                    data = data[offset:(offset+limit)]
                else:
                    data = data[offset:]
        if "limit" in attributes and 'offset' not in attributes:
            limit = int(attributes['limit'])
            data = data[:limit]
        return str(data)
    else:
        return db.get_db_data_cats(get_db)


def post_validation(request_data):
    try:
        json.loads(request_data)
    except ValueError:
        return "Invalid JSON"
    data = json.loads(request_data.decode('utf-8'))
    current_names = [i['name'] for i in json.loads(db.get_db_data_cats(get_db))]
    if data['name'] in current_names:
        return f"{data['name']} is already added"
    if type(data['tail_length']) not in (int, float):
        return "tail_length must be float or integer"
    if data['tail_length'] < 0:
        return f"tail_length cannot be negative "
    if type(data['whiskers_length']) not in (int, float):
        return "'whiskers_length must be float or integer"
    if data['whiskers_length'] < 0:
        return "whiskers_length cannot be negative"
    return None


@app.post("/cat")
def post_cat():
    json_data = request.get_data()
    if post_validation(json_data) is None:
        data = json.loads(json_data.decode('utf-8'))
        db.post_db_data_cats(data, get_db)
        return f"{data['name']} added"
    else:
        return post_validation(json_data)


if __name__ == "__main__":
    app.run(host="localhost", port=8080)
