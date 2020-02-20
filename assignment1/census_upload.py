import psycopg2
import sys
import pandas as pd
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--file_path', type=str)
parser.add_argument('--sch_name', type=str)
parser.add_argument('--tb_name', type=str)
parser.add_argument('--user', type=str)
parser.add_argument('--password', type=str)

# Creates schema
def create_schema(sch_name, tb_name, cursor, conn):
    query="CREATE SCHEMA IF NOT EXISTS {0}; DROP TABLE IF EXISTS {0}.{1};".format(sch_name, tb_name)
    cursor.execute(query)
    conn.commit()

# Creates table based on csv
def create_table(sch_name, tb_name, data, cursor, conn):
    query = "CREATE TABLE IF NOT EXISTS {}.{} ( pk VARCHAR PRIMARY KEY, ".format(sch_name, tb_name)
    data_columns = [col for col in data.columns if col != 'pk']
    for i, col in enumerate(data_columns):
        # Columns
        col_type=data.dtypes[i+1]
        if col_type == 'int64':
            postgres_type = 'INT'
        elif col_type == 'float64':
            postgres_type = 'NUMERIC'
        else:
            postgres_type = 'VARCHAR'
        string_var = "{} {} NULL".format(col, postgres_type)

        if i==0:
            query = query + string_var
        else:
            query = query + ", " + string_var
    query = query + ")"

    cursor.execute(query)
    conn.commit()

# Upload data
def upload_data(sch_name, tb_name, file_path, cursor, conn):
    table = "{}.{}".format(sch_name, tb_name)
    f = open(file_path, 'r')
    next(f) # skips header
    cursor.copy_from(f, table, sep=',', null='None')
    f.close()
    conn.commit()

def main(args):
    conn_string = "host='mlpolicylab.db.dssg.io' dbname='o1_database' user='{}' password='{}'".format(args.user, args.password)
    print("Connecting to database\n     {0}".format(conn_string))

    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    print("Connected!\n")

    # Reads data from file
    print("Reading data...")
    data = pd.read_csv(args.file_path)

    # Create/check schrma
    print("Creating schema...")
    create_schema(sch_name=args.sch_name, tb_name=args.tb_name, cursor=cursor, conn=conn)

    # Create data
    print("Creating table...")
    create_table(sch_name=args.sch_name, tb_name=args.tb_name, data=data, cursor=cursor, conn=conn)

    # Upload data
    print("Uploading data...")
    upload_data(sch_name=args.sch_name, tb_name=args.tb_name, file_path=args.file_path, cursor=cursor, conn=conn)

if __name__ == '__main__':
    args = parser.parse_args()
    main(args)
