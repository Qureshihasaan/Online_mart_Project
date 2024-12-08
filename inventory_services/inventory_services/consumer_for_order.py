# from aiokafka import AIOKafkaConsumer , AIOKafkaProducer
# import asyncio , logging , json
# from . import setting
# from sqlmodel import Session
# from .database import engine
# from .model import Stock_update
# from .Producer_for_order import producer_for_order_process


# loop = asyncio.get_event_loop()
# logging.basicConfig(level=logging.INFO)


# async def check_inventory():
#     consumer = AIOKafkaConsumer(
#         setting.KAFKA_ORDER_TOPIC,
#         loop=loop,
#         bootstrap_servers=setting.BOOTSTRAP_SERVER,
#         group_id=setting.KAFKA_CONSUMER_GROUP_ID_FOR_INVENTORY,
#         auto_offset_reset="earliest",
#         value_deserializer=lambda x: json.loads(x.decode("utf-8")),
#     )
#     try:
#         await consumer.start()
#         logging.info("Consumer Started For Inventory Checking...")
#     except Exception as e:
#         logging.warning("Consumer Starting Failed, Retry in 5 sec...")
#         await asyncio.sleep(5)

#     try:
#         async for msg in consumer:
#             event = json.loads(msg.value.decode("utf-8"))
#             print(f"event received: {event}")
#             print(type(event))
#             if event["event_type"] == "Order_Created":
#                 data = event.get("order", {})
#                 product_id = data.get("product_id")
#                 order_quantity = data.get("product_quantity")
#                 if product_id & order_quantity == None:
#                     logging.warning("Product ID & Order Quantity not found in event. Skipping...")
#                     continue
#                 with Session(engine) as session:
#                     product = session.query(Stock_update).filter(Stock_update.product_id == product_id).first()
#                     if product:
#                         if product.product_quantity >= order_quantity:
#                             product.product_quantity -= order_quantity
#                             session.commit()
#                             logging.info(f"Inventory updated for product {product_id}")
#                         else:
#                             logging.warning(f"Insufficient inventory for product {product_id}")
                           

#             elif event["event_type"] == "Order_Deleted":
#                 data = event.get("order", {})
#                 product_id = data.get("product_id")
#                 order_quantity = data.get("product_quantity")
#                 if product_id & order_quantity == None:
#                     logging.warning("Product ID & Order Quantity not found in event. Skipping...")
#                     continue
#                 with Session(engine) as session:
#                     product = session.query(Stock_update).filter(Stock_update.product_id == product_id).first()
#                     if product:
#                         product.product_quantity += order_quantity
#                         session.commit()
#                         logging.info(f"Inventory updated for product {product_id}")
#                         continue
#                         await producer_for_order_process()
#     finally:
#         await consumer.stop()
#         logging.info("Consumer Stopped...")
    




# async def handle_order_created(event):
#     data = event.get("order", {})
#     product_id = data.get("product_id")
#     order_quantity = data.get("product_quantity")
#     if product_id is None or order_quantity is None:
#         logging.warning("Product ID & Order Quantity not found in event. Skipping...")
#         return
#     with Session(engine) as session:
#         product = session.query(Stock_update).filter(Stock_update.product_id == product_id).first()
#         if product:
#             if product.product_quantity >= order_quantity:
#                 product.product_quantity -= order_quantity
#                 session.commit()
#                 logging.info(f"Inventory updated for product {product_id}")

#                 await producer_for_order_process(
#                     event_type = "Inventory_updated",
#                     order_id = event["order"]["order_id"],
#                     status = "Success"
#                 )
            
#             else:
#                 logging.warning(f"Insufficient inventory for product {product_id}")

#                 await producer_for_order_process(
#                     event_type = "Inventory_updated",
#                     order_id = event["order"]["order_id"],
#                     status = "Failed"
#                 )


# async def handle_order_deleted(event):
#     data = event.get("order", {})
#     product_id = data.get("product_id")
#     order_quantity = data.get("product_quantity")
#     if product_id is None or order_quantity is None:
#         logging.warning("Product ID & Order Quantity not found in event. Skipping...")
#         return
#     with Session(engine) as session:
#         product = session.query(Stock_update).filter(Stock_update.product_id == product_id).first()
#         if product:
#             product.product_quantity += order_quantity
#             session.commit()
#             logging.info(f"Inventory updated for product {product_id}")

#             await producer_for_order_process(
#                 event_type = "Inventory_updated",
#                 order_id = event["order"]["order_id"],
#                 status = "Replenished"
#             )