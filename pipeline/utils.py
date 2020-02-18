import psycopg2
import pandas as pd
import pandas.io.sql as sqlio
from datetime import datetime

def _download_table(tb_name, conn):
    sql = "select * from {};".format(tb_name)
    return sqlio.read_sql_query(sql, conn)

def download_data(user, password, tb_name, port=8888):
    #Define our connection string
    conn_string = "host='localhost' dbname='o1_database' user='{}' password='{}' port='{}'".format(user, password, port)

    # print the connection string we will use to connect
    print("Connecting to database\n	{0}".format(conn_string))

    # get a connection, if a connect cannot be made an exception will be raised here
    conn = psycopg2.connect(conn_string)

    # conn.cursor will return a cursor object, you can use this cursor to perform queries
    cursor = conn.cursor()
    print("Connected!\n")

    data = _download_table(tb_name, conn)

    return data

def upload_result(model_name, metric, user, password, port=8888):
    #Define our connection string
    conn_string = "host='localhost' dbname='o1_database' user='{}' password='{}' port='{}'".format(user, password, port)

    # print the connection string we will use to connect
    print("Connecting to database\n	{0}".format(conn_string))

    # get a connection, if a connect cannot be made an exception will be raised here
    conn = psycopg2.connect(conn_string)

    # conn.cursor will return a cursor object, you can use this cursor to perform queries
    cursor = conn.cursor()
    print("Connected!\n")

    query = "INSERT INTO sketch.model_evaluation(model_name, time_stamp, user_name, metric) VALUES ('{}', '{}', '{}', '{}');".format(model_name, datetime.now(), user, metric)

    cursor.execute(query)
    conn.commit()