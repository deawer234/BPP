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
# Execute the SQL statement

session = scoped_session(sessionmaker(autocommit=False,
                                        autoflush=False,
                                        bind=engine))


# session.execute(text('''INSERT INTO Movement (name) VALUES('tab1') '''))
# session.execute(text(''' INSERT INTO Movement (name) VALUES('tab2') '''))

# session.execute(text('''INSERT INTO Position (movement_id, base, shoulder, elbow, wrist, wrist_rot, gripper) VALUES(1, 45, 125, 50, 50, 50, 50)'''))
# session.execute(text('''INSERT INTO Position (movement_id, base, shoulder, elbow, wrist, wrist_rot, gripper) VALUES(2, 86, 40, 50, 50, 50, 50)'''))
# session.execute(text('''INSERT INTO Position (movement_id, base, shoulder, elbow, wrist, wrist_rot, gripper) VALUES(2, 12, 40, 50, 69, 50, 50)'''))
Base = declarative_base()
Base.query = session.query_property()

SQLALCHEMY_COMMIT_ON_TEARDOWN = True

def init_db():
    import website.model.position_model
    import website.model.movement_model 
    Base.metadata.create_all(bind=engine)