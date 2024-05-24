import json


def get_cats(conn):
    with conn.cursor() as curs:
        query_request = 'SELECT * FROM public.cats;'
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
    with conn.cursor() as curs:
        query_request = f"INSERT into cats (name, color, tail_length, whiskers_length) values {input_data['name'], input_data['color'], input_data['tail_length'], input_data['whiskers_length']};"
        curs.execute(
            query_request
        )


def get_db_data_cats(conn):
    with conn() as database_connection:
        result = get_cats(database_connection)
        return result


def post_db_data_cats(input_data, conn):
    with conn() as database_connection:
        post_cats(database_connection, input_data)
