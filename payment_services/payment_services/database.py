from datetime import datetime
from sqlmodel import SQLModel , Field, Session , create_engine
from . import setting


connection_string = str(setting.DATA_BASE_URL).replace(
    "postgresql" , "postgresql+psycopg2"
)

engine = create_engine(connection_string , pool_recycle=300 , connect_args={})


def create_db_and_tables()->None:
    SQLModel.metadata.create_all(engine)


def get_db():
    with Session(engine) as session:
        yield session