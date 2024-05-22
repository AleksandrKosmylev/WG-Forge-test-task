import json
import os
from operator import itemgetter

from flask import request
from flask import Flask
import psycopg2
from psycopg2.extras import NamedTupleCursor


app = Flask(__name__)

# DATABASE_URL="postgres://wbveoezi:u6ASwE-0rCKJMuNoRF9sWB4YAZGQcFDQ@cornelius.db.elephantsql.com/wbveoezi"
conn = psycopg2.connect(dbname="wg_forge_db", user="wg_forge", password="a42", host="localhost", port="5432")
# conn = psycopg2.connect(DATABASE_URL)


def get_db():
    # return psycopg2.connect(app.config['DATABASE_URL'])
    return psycopg2.connect(dbname="wg_forge_db", user="wg_forge", password="a42", host="localhost", port="5432")


def get_cats(conn):
    with conn.cursor() as curs:
        query_request = 'SELECT * FROM cats;'
        curs.execute(
            query_request
        )
        cats = curs.fetchall()
        res = []
        for row in cats:
            d = {}
            for i, col in enumerate(curs.description):
                d[col[0]] = row[i]
            res.append(d)
        json_result = json.dumps(res)
        return json_result


def post_cats(conn, input_data):
    print(input_data,  '2 step')
    with conn.cursor() as curs:
        print(input_data)
        # "INSERT into cats (name, color, tail_length, whiskers_length) values ('Tihon', 'red & white', 15, 12);"
        query_request = f"INSERT into cats (name, color, tail_length, whiskers_length) values {input_data['name'], input_data['color'], input_data['tail_length'], input_data['whiskers_length']};"
        curs.execute(
            query_request
        )


def get_db_data_cats():
    with get_db() as database_connection:
        result = get_cats(database_connection)
        return result


def post_db_data_cats(input_data):
    print(input_data, "1step")
    with get_db() as database_connection:
        post_cats(database_connection, input_data)


@app.route('/')
def hello_world():
    return 'Welcome to Flask!'


@app.route("/ping")
def ping():
    return "Cats Service. Version 0.1"


@app.route("/cats", methods=['GET'])
def show_cats():
    error = None
    val = request.values
    if val and val != '':
        print(val)
        list_of_cats = get_db_data_cats()
        data = json.loads(list_of_cats)
        table_keys = list(data[0])
        len_of_list = len(data)
        if "attribute" in val:
            if val['attribute'] in table_keys:
                if val['order'] == 'asc':
                    data = sorted(data, key=lambda d: d[val['attribute']], reverse=False)
                elif val['order'] == 'desc':
                    data = sorted(data, key=lambda d: d[val['attribute']], reverse=True)
                else:
                    error = " Order attribute is incorrect"
                    return error
            else:
                error = "Attribute is incorrect"
                return error
        if "offset" in val:
            offset = int(val["offset"])
            if offset >= len_of_list:
                error = " Check offset value. Value is too big"
                return error
            else:
                if 'limit' in val:
                    limit = int(val['limit'])
                    data = data[offset:(offset+limit)]
                else:
                    data = data[offset:]
        if "limit" in val and 'offset' not in val:
            limit = int(val['limit'])
            data = data[:limit]
        return str(data)
    else:
        return get_db_data_cats()


def post_validation(request_data):
    try:
        json.loads(request_data)
    except ValueError as err:
        return "Invalid JSON"
    data = json.loads(request_data.decode('utf-8'))
    current_names = [i['name'] for i in json.loads(get_db_data_cats())]
    if data['name'] in current_names:
        return f"{data['name']} is already  in list"
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
        post_db_data_cats(data)
        return f"{data['name']} added"
    else:
        return post_validation(json_data)


if __name__ == "__main__":
    app.run(host="localhost", port=8080)

# search?query=str.lower&opt=9:
"""
curl -X GET http://localhost:8080/cats?attribute=name&order=asc
curl -X GET http://localhost:8080/cats?attribute=tail_length&order=desc
curl -X GET http://localhost:8080/cats?offset=10&limit=10
curl -X GET http://localhost:8080/cats?attribute=color&order=asc&offset=5&limit=2


curl -X POST http://localhost:8080/cat \
-d "{\"name\": \"Tihon\", \"color\": \"red & white\", \"tail_length\": 15, \"whiskers_length\": 12}"
curl -X POST http://127.0.0.1:8080/cat \
-d "{\"name\": \"Tihon\", \"color\": \"red & white\", \"tail_length\": 15, \"whiskers_length\": 12}"


curl -X POST http://127.0.0.1:8000/cats -d "{\"name\": \"Tihon\", \"color\": \"red & white\", \"tail_length\": 15, \"whiskers_length\": 12}"
curl -X POST http://127.0.0.1:8000/cats -d "{\"name\": \"Tihon\", \"color\": \"red & white\", \"tail_length\": 15, \"whiskers_length\": 12}"


curl -X POST http://127.0.0.1:8000/cat \-d "{\"name\": \"Tihon\", \"color\": \"red & white\", \"tail_length\": 15, \"whiskers_length\": 12}"

"""
