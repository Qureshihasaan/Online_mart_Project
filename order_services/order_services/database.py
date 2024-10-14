from sqlmodel import SQLModel, Field , create_engine
from .setting import DATA_BASE_URL
# from ...product_services.product_services.database import product_id
from typing import Optional


class Order(SQLModel , table=True):
    order_id : Optional[int] = Field(default=None , primary_key=True)
    product_id : int 
    product_name : str = Field(default=None)
    product_price : int = Field(default = None)
    product_quantity : int = Field(default=None)


connection_string = str(DATA_BASE_URL).replace(
    "postgresql" , "postgresql+psycopg2"
)

engine = create_engine(connection_string , connect_args={} , pool_recycle=300)


def create_db_and_tables()->None:
    SQLModel.metadata.create_all(engine)


