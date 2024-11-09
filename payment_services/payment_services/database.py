from sqlmodel import SQLModel , Field, Session , create_engine
from .setting import DATA_BASE_URL

connection_strings = str(DATA_BASE_URL).replace(
    "postgresql" , "postgresql+psycopg2"
)

engine = create_engine(connection_strings , connect_args={} , pool_recycle=300) 


def create_db_and_tables()->None:
    SQLModel.metadata.create_all(engine)


def get_db():
    with Session(engine) as session:
        yield session