"""
Module for establishing communication with the database

Author: Daniel Němec
Date: 01.04.2023

Python Version: 3.8.10
"""

from sqlalchemy import create_engine, text
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.pool import StaticPool

db_file = 'sqlite:///./website/database/db.db'
sql_file = "./website/database/db.sqlite"

engine = create_engine('sqlite:///./website/database/db.db', connect_args={'check_same_thread': False}, poolclass=StaticPool)

session = engine.connect()

# Read the contents of the SQL file
with engine.connect() as session:
    with open(sql_file, 'r') as f:
        sql_script = f.read()
        sql_statements = sql_script.split(';')
        for sql_statement in sql_statements:
            if sql_statement.strip() != '':
                sql_expression = text(sql_statement)
                session.execute(sql_expression)

session = scoped_session(sessionmaker(autocommit=False,
                                        autoflush=False,
                                        bind=engine))

Base = declarative_base()
Base.query = session.query_property()

SQLALCHEMY_COMMIT_ON_TEARDOWN = True

def init_db():
    import website.model.position_model
    import website.model.movement_model 
    Base.metadata.create_all(bind=engine)