from sqlmodel import SQLModel , create_engine , Session  
from .setting import DATA_BASE_URL



connection_strings = str(DATA_BASE_URL).replace(
    "postgresql" , "postgresql+psycopg2"
)

engine = create_engine(connection_strings , connect_args={} ,  pool_recycle=300)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session



