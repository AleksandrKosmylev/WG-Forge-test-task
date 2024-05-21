import json
import os
from operator import itemgetter
from urllib import request

from flask import Flask
import psycopg2
from psycopg2.extras import NamedTupleCursor


app = Flask(__name__)

# DATABASE_URL="postgres://wbveoezi:u6ASwE-0rCKJMuNoRF9sWB4YAZGQcFDQ@cornelius.db.elephantsql.com/wbveoezi"
conn = psycopg2.connect(dbname="wg_forge_db", user="wg_forge", password="a42", host="localhost", port="5432") 
#conn = psycopg2.connect(DATABASE_URL)

"""
cursor = conn.cursor()
query = "SELECT * FROM cats"
cursor.execute(query)
result = cursor.fetchall()
res = []
for row in result:
    d = {}
    for i, col in enumerate(cursor.description):
        d[col[0]] = row[i]
        res.append(d)
json_result = json.dumps(res)
print(json_result)
conn.close()
"""

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
            # print(row)
            d = {}
            for i, col in enumerate(curs.description):
                # print(i,  col)
                d[col[0]] = row[i]
            res.append(d)
        json_result = json.dumps(res)
        # print(json_result, 'ss')
        return json_result

def get_db_data_cats(conn):
    with conn() as database_connection:
        result = get_cats(database_connection)
        # extracted_from_urls_checks_table = [i[0] for i in result_url]
        # urls_checks_data = get_check_and_response(extracted_from_urls_checks_table, database_connection)
        # return result_url, urls_checks_data
        return result



@app.route('/')
def hello_world():
    return 'Welcome to Flask!'


@app.route("/ping")
def ping():
    return "Cats Service. Version 0.1"


@app.route("/cats")
def show_cats():
    error = None
    val = request.values
    if val and val != '':
        print(val)
        list_of_cats = get_db_data_cats(get_db)
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
        return get_db_data_cats(get_db)

    
    """
    conn = psycopg2.connect(dbname="wg_forge_db", user="wg_forge", password="a42", host="localhost", port="5432")

    cursor = conn.cursor()
    query = "SELECT * FROM cats"
    cursor.execute(query)
    result = cursor.fetchall()
    res = []
    for row in result:
        d = {}
        for i, col in enumerate(cursor.description):
            d[col[0]] = row[i]
            res.append(d)
    json_result = json.dumps(res)
    conn.close()
    return json_result
    """

"""
    #conn = psycopg2.connect(dbname="wg_forge_db", user="wg_forge", password="a42", host="localhost", port="5432")
    conn = get_db()
    cursor = conn.cursor()
    query = "SELECT * FROM cats"
    cursor.execute(query)
    result = cursor.fetchall()
    res = []
    for row in result:
        d = {}
        for i, col in enumerate(cursor.description):
            d[col[0]] = row[i]
            res.append(d)
    json_result = json.dumps(res)
    conn.close()
    return json_result
"""


from flask import request

@app.route('/search/', methods=['GET'])
def search():
    error = None
    query = request.args.get('query')
    # проверяем, передается ли параметр
    # 'query' в URL-адресе
    if query and query != '':
        # если `query`существует и это не пустая строка,
        # то можно приступать к обработке запроса
        opt = request.args.get('opt', default=0, type=int)
        # возвратит `query=str.lower, opt=9`
        return f"query={query}, opt={opt}"
    else:
        # если `query` не существует или это пустая строка, то 
        # отображаем форму поискового запроса с сообщением.
        error = 'Не введен запрос!'
        # return render_template('search.html', error=error)
        return error

if __name__ == "__main__":
    app.run(host="localhost", port=8080)

# search?query=str.lower&opt=9:
"""
curl -X GET http://localhost:8080/cats?attribute=name&order=asc
curl -X GET http://localhost:8080/cats?attribute=tail_length&order=desc
curl -X GET http://localhost:8080/cats?offset=10&limit=10
curl -X GET http://localhost:8080/cats?attribute=color&order=asc&offset=5&limit=2
"""


"""
@app.route("/cats")
def show_cats():
    error = None
    # attribute = request.args.get('attribute')
    val = request.values
    if val and val != '':
        list_of_cats = get_db_data_cats(get_db)
        data = json.loads(list_of_cats)
        if "attribute" in val:
            ordering = val['order']
            if ordering == 'asc' or ordering == 'desc':

                print('asc')
                # newlist = sorted(data, key=lambda d: d[val['attribute']], reverse=False)
            elif val['order'] == 'desc':
                print('desc')
                newlist = sorted(data, key=lambda d: d[val['attribute']], reverse=True)

        if "offset" in val or 'limit' in val:
            offset = val["offset"]
            limit = val['limit']

        get_db_data_cats(get_db, ordering, offset)

        return newlist
        # return [val['order'], val["attribute"]]
        # list_of_cats.sort(key=lambda x: x["name"])
    else:
        return get_db_data_cats(get_db)
"""