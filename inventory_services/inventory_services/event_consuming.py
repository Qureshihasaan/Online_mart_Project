# from .conusmer import consume_message
# from .model import Stock_update
# from .main import get_db
# import json

# def process_inventory_event(event):
#     event_type = event.get("event_type")
#     product_id = event.get("product_id")
#     product_name = event.get("product_name")
#     product_price = event.get("product_price")


#     if event_type == "product_created":
#         print(f"Inventory Service: Adding new product to inventory: {product_id} - {product_name}")
#         add_to_inventory(product_id, product_name, product_price)
#     elif event_type == "product_updated":
#         print(f"Inventory Service: Updating product in inventory: {product_id} - {product_name}")
#         update_inventory(product_id, product_name, product_price)
#     elif event_type == "product_deleted":
#         print(f"Inventory Service: Removing product from inventory: {product_id} - {product_name}")
#         remove_from_inventory(product_id)
#     else:
#         print(f"Inventory Service: Unknown event type: {event_type}")


# # Initialize a new database session

# def add_to_inventory(product_id, product_name, product_price, stock_quantity=0):
#     db = next(get_db())
#     # Check if product already exists
#     existing_product = db.query(Stock_update).filter(Stock_update.product_id == product_id).first()
#     if existing_product:
#         print(f"Product with ID {product_id} already exists in inventory.")
#         return
#     # Create new product entry
#     new_product = Stock_update(
#         product_id=product_id,
#         product_name=product_name,
#         product_price=product_price,
#         stock_quantity=stock_quantity
#     )
#     db.add(new_product)
#     db.commit()
#     db.refresh(new_product)
#     print(f"Added to inventory: {product_id} - {product_name} - ${product_price}")

# def update_inventory(product_id, product_name=None, product_price=None, stock_quantity=None):
#     db = next(get_db())
#     # Find the product in the database
#     product = db.query(Stock_update).filter(Stock_update.product_id == product_id).first()
#     if not product:
#         print(f"Product with ID {product_id} not found in inventory.")
#         return
#     # Update product details
#     if product_name:
#         product.product_name = product_name
#     if product_price:
#         product.product_price = product_price
#     if stock_quantity is not None:
#         product.stock_quantity = stock_quantity
#     db.commit()
#     db.refresh(product)
#     print(f"Updated in inventory: {product_id} - {product_name or product.product_name} - ${product_price or product.product_price}")

# def remove_from_inventory(product_id):
#     db = next(get_db())
#     # Find and delete the product
#     product = db.query(Stock_update).filter(Stock_update.product_id == product_id).first()
#     if not product:
#         print(f"Product with ID {product_id} not found in inventory.")
#         return
#     db.delete(product)
#     db.commit()
#     print(f"Removed from inventory: {product_id}")


# for message in consume_message:
#     event = message.value
#     process_inventory_event(event)

from aiokafka import AIOKafkaConsumer
import json

def handle_product_event(event_data):
    if event_data["event_type"] == "product_created":
        print(f"Product created: {event_data}")
    elif event_data["event_type"] == "product_updated":
        print(f"Product updated: {event_data}")
    elif event_data["event_type"] == "product_deleted":
        print(f"Product deleted: {event_data}")


async def consume_product_events(consumer:AIOKafkaConsumer):
    async for msg in consumer:
        event_data = json.loads(msg.value.decode("utf-8"))
        handle_product_event(event_data)