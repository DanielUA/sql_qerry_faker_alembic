from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# an Engine, which the Session will use for connection
# resources, typically in module scope
POSTGRESS_URL = "postgresql+psycopg2://postgres:example@localhost:5432/postgres"
engine = create_engine(POSTGRESS_URL)

# a sessionmaker(), also in the same scope as the engine
Session = sessionmaker(engine)

def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()

# we can now construct a Session() without needing to pass the
# # engine each time
# with Session() as session:
#     session.add(some_object)
#     session.add(some_other_object)
#     session.commit()
# closes the session