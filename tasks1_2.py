from service.server import get_db


first_task_request = 'INSERT INTO public.cat_colors_info (color, count) SELECT color, COUNT(color) FROM public.cats GROUP BY color; SELECT * FROM cat_colors_info ;'
second_task_request = """INSERT INTO public.cats_stat (tail_length_mean, tail_length_median, tail_length_mode, whiskers_length_mean, whiskers_length_median, whiskers_length_mode)
SELECT
    (SELECT AVG(tail_length) FROM public.cats),
    (SELECT percentile_cont(0.5) WITHIN GROUP (ORDER BY tail_length) FROM public.cats),
    (SELECT array_agg(tail_length) FROM (SELECT tail_length, COUNT(tail_length) AS count FROM public.cats GROUP BY tail_length HAVING COUNT(tail_length) = (SELECT MAX(cnt) FROM (SELECT COUNT(tail_length) AS cnt FROM public.cats GROUP BY tail_length) AS t) ORDER BY tail_length) AS values),
    (SELECT AVG(whiskers_length) FROM public.cats),
    (SELECT mode() WITHIN GROUP (ORDER BY whiskers_length) AS modal_value FROM public.cats),
    (SELECT array_agg(whiskers_length) FROM (SELECT whiskers_length, COUNT(whiskers_length) AS count FROM public.cats GROUP BY whiskers_length HAVING COUNT(whiskers_length) = (SELECT MAX(cnt) FROM (SELECT COUNT(whiskers_length) AS cnt FROM public.cats GROUP BY whiskers_length) AS t) ORDER BY whiskers_length) AS values);"""


def handle_request(conn, raw_request):
    with conn.cursor() as curs:
        query_request = raw_request
        curs.execute(
            query_request
        )


def connect_db(raw_request):
    with get_db() as database_connection:
        handle_request(database_connection, raw_request)
    print("Data added")


connect_db(first_task_request)
connect_db(second_task_request)
