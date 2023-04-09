import sqlite3
from sqlite3 import Connection

def get_connection(db_file: str) -> Connection:
    return sqlite3.connect(db_file, isolation_level=None)

def create_database(db_file: str, sql_file: str):
    # read the SQL code from the file
    with open(sql_file, 'r') as f:
        sql_code = f.read()

    # get a connection from the connection pool
    conn = get_connection(db_file)

    # create a cursor object to execute SQL queries
    cursor = conn.cursor()

    # execute the SQL code to create the database and table
    cursor.executescript(sql_code)

    # commit the changes to the database
    conn.commit()
