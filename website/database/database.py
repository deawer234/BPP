import sqlite3
from sqlite3 import Connection
db_file = "./db.db"
sql_file = "./db.sqlite"
def get_connection() -> Connection:
    return sqlite3.connect(db_file, isolation_level=None)

def create_database():
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
