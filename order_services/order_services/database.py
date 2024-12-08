from sqlmodel import SQLModel, Field , create_engine , Session
from .setting import DATA_BASE_URL
from typing import Optional
from pydantic import EmailStr 

class Order(SQLModel , table=True):
    order_id : Optional[int] = Field(default=None, primary_key=True)
    user_id : int 
    # order_id : Optional[int] = Field(default=None , primary_key=True)
    user_email : EmailStr = Field(index=True , nullable=False , unique=True)
    product_id : int 
    total_amount : int = Field(default = None)
    product_quantity : int = Field(default=None)
    payment_status : str = Field(default="Pending")



class Order_request(SQLModel):
    order_id : int
    product_id : int
    product_quantity : int
    total_amount : int

class OrderResponse(SQLModel):
    order_id : int
    user_id : int
    product_id : int
    total_amount : int
    product_quantity : int
    payment_status : str


class User(SQLModel):
    # id : Optional[int] = Field(default=None , primary_key=True, index=True)
    username : str = Field(index=True , unique=True , nullable=False)
    # email : EmailStr = Field(index=True, nullable=False , unique=True)
    hashed_password : str

class create_user(SQLModel):
    username : str
    password : str

# class User(BaseModel):
#     username : str
#     password : str


connection_string = str(DATA_BASE_URL).replace(
    "postgresql" , "postgresql+psycopg2"
)

engine =create_engine(connection_string , connect_args={} , pool_recycle=300)


def create_db_and_tables()->None:
    SQLModel.metadata.create_all(engine)




def get_db():
    with Session(engine) as session:
        yield session
