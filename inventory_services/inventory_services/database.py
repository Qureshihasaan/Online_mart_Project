from sqlmodel import SQLModel , Field , create_engine
from typing import  Optional
from .setting import DATABASE_URL
    
    

    
connection_string = str(DATABASE_URL).replace(
    "postgresql" , "postgresql+psycopg2"
)

engine = create_engine(connection_string , connect_args={} , pool_recycle=300)

def create_db_and_tables()-> None:
   SQLModel.metadata.create_all(engine) 