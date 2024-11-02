from sqlmodel import SQLModel , Field
from typing import Optional
# from datetime import datetime
import uuid



class Payment(SQLModel , table=True):
    id : Optional[int] = Field(default_factory=lambda:str(uuid.uuid4()) , primary_key=True)
    user_id : str 
    order_id : str 
    amount : str 
    status : str         ### Pending    Completed      Failed
    # created_at : datetime = Field(default_factory=datetime.utcnow)
    # updated_at : datetime = Field(default_factory=datetime.utcnow)