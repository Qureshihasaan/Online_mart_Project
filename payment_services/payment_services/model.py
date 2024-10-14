from sqlmodel import SQLModel , Field
from typing import Optional
from datetime import datetime

class Payment(SQLModel , table=True):
    id : Optional[int] = Field(default=None , primary_key=True)
    user_id : int 
    order_id : int 
    amount : int 
    status : str            ### Pending    Completed      Failed
    created_at : datetime = Field(default_factory=datetime.utcnow)
    updated_at : datetime = Field(default_factory=datetime.utcnow)