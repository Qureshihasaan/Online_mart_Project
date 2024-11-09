# from .conusmer import consume_message
# from .database import engine 
# from .model import Stock_update
# from sqlmodel import Session
# import json


# def consume_created_product():
#     for msg in consume_message():
#         print("msg" , msg)
#         try:
#             data = json.loads(msg.value.decode("utf-8"))
#             product_id = data["product_id"]
#             with Session(engine) as session:
#                 inventory_item= session.query(Stock_update).filter(Stock_update.product_id == product_id).first()
#                 if not inventory_item: 
#                     inventory_item = Stock_update(product_id=product_id, product_quantity=10)
#                     session.add(inventory_item)
#                     print(f"Adding Inventory item for product_id: {product_id}" )
#                 else:
#                     print(f"Inventory item already exists for product_id: {product_id}")
#                 session.commit()
          
#         except Exception as e:
#             print(f"Error processing message: {e}")