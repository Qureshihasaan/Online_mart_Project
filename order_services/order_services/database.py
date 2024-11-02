from sqlmodel import SQLModel, Field , create_engine
from .setting import DATA_BASE_URL
from typing import Optional

class Order(SQLModel , table=True):
    id : Optional[int] = Field(default=None, primary_key=True)
    user_id : int 
    # order_id : Optional[int] = Field(default=None , primary_key=True)
    product_id : int 
    total_amount : int = Field(default = None)
    product_quantity : int = Field(default=None)
    payment_status : str = Field(default="Pending")



class Order_request(SQLModel):
    order_id : int
    product_quantity : str
    payment_status : str
    total_amount : int


connection_string = str(DATA_BASE_URL).replace(
    "postgresql" , "postgresql+psycopg2"
)

engine =create_engine(connection_string , connect_args={} , pool_recycle=300)


def create_db_and_tables()->None:
    SQLModel.metadata.create_all(engine)


