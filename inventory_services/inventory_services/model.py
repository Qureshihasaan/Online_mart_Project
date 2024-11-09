from sqlmodel import SQLModel , Field


class Stock_update(SQLModel , table = True):
    id : int = Field(default=None, primary_key=True)
    product_id : int 
    product_name : str
    product_quantity : int 
    status : str = Field(default="In Stock")
    
    
class Inventory_update(SQLModel):
    product_id : int = None
    product_quantity : int = None
    status : str = None
    