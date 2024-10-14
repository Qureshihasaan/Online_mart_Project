from sqlmodel import SQLModel , Field


class Stock_update(SQLModel , table = True):
    id : int = Field(default=None, primary_key=True)
    product_id : int 
    product_name : str
    product_stock : int 
    status : str
    
    
class Inventory_update(SQLModel):
    product_id : int = None
    product_stock : int = None
    status : str = None
    