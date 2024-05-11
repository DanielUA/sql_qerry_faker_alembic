from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from seed import fill_data

# an Engine, which the Session will use for connection
# resources, typically in module scope
POSTGRES_URL = "postgresql+psycopg2://postgres:example@localhost:5432/postgres"
engine = create_engine(POSTGRES_URL)

# a sessionmaker(), also in the same scope as the engine
Session = sessionmaker(engine)

# create a session instance
session = Session()

# call the fill_data function with the session instance
fill_data(session)

# commit changes to the database
session.commit()

# close the session
session.close()

def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()
