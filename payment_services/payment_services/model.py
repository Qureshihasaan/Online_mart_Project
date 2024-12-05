from sqlmodel import SQLModel , Field
from typing import Optional
from pydantic import EmailStr



class Payment(SQLModel , table=True):
    payment_id : Optional[int] = Field(index=True, primary_key=True)
    # user_email : str 
    order_id : int 
    amount : float 
    status : str = Field(default="Pending")       ### Pending    Completed      Failed
    

class payment_response(SQLModel):
    payment_id : int
    order_id : int
    amount : float
    status : str