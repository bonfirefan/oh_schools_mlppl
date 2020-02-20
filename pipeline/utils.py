import psycopg2
import pandas as pd
import pandas.io.sql as sqlio
from datetime import datetime

def _download_table(conn, tb_name):
    sql = "select * from {};".format(tb_name)
    return sqlio.read_sql_query(sql, conn)

def download_data(user, password, tb_name, port=8888):
    conn_string = "host='localhost' dbname='o1_database' user='{}' password='{}' port='{}'".format(user, password, port)
    try:
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor()
        print("Connected!\n")

        data = _download_table(conn, tb_name)
        conn.close()
    except:
        pass
    return data

def upload_result(model_name, metric_name, value, user, password, port=8888):
    conn_string = "host='localhost' dbname='o1_database' user='{}' password='{}' port='{}'".format(user, password, port)
    conn = psycopg2.connect(conn_string)
    try:
        cursor = conn.cursor()
        print("Connected!\n")

        query = "INSERT INTO sketch.model_evaluation(id, model_name, time_stamp, user_name, metric, value) VALUES (nextval('sketch.model_sequence'),'{}', '{}', '{}', '{}','{}');".format(model_name, datetime.now(), user, metric_name, value)

        cursor.execute(query)
        conn.commit()
        conn.close()
    except:
        pass
