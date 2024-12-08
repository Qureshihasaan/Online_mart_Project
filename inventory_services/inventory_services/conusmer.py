import asyncio, logging 
from aiokafka import AIOKafkaConsumer
from aiokafka.errors import KafkaConnectionError
from . import setting
from .database import engine
from sqlmodel import Session
from .model import Stock_update , Inventory_update
import json


loop = asyncio.get_event_loop()
logging.basicConfig(level=logging.INFO)


# async def consume_message():
#     consumer = AIOKafkaConsumer(
#         setting.KAFKA_PRODUCT_TOPIC,
#         bootstrap_servers=setting.BOOTSTRAP_SERVER,
#         group_id=setting.KAFKA_CONSUMER_GROUP_ID_FOR_INVENTORY,
#         auto_offset_reset="earliest",
#         value_deserializer= lambda x: json.loads(x.decode("utf-8"))
async def consume_product_events():
    consumer = AIOKafkaConsumer(
        setting.KAFKA_INVENTORY_TOPIC,
        bootstrap_servers=setting.BOOTSTRAP_SERVER,
        group_id=setting.KAFKA_CONSUMER_GROUP_ID_FOR_INVENTORY,
        auto_offset_reset="earliest",
        # value_deserializer=lambda x: json.loads(x.decode("utf-8"))
    )
    await consumer.start()
    print("Consumer started...")
    try:
        async for msg in consumer:
            event = json.loads(msg.value.decode("utf-8"))
            print(type(event))
            print("Event received:", event)
            if event["event_type"] == "Product_Created":
                product = event["product"]
                add_inventory(product["product_id"] ,product["Product_name"] , product["product_quantity"] )
                print("Product added to inventory..")

            elif event["event_type"] == "Product_Updated":
                product = event["product"]
                update_inventory(
                    product["product_id"],
                    product["Product_name"],
                    product["product_quantity"]
                )
                print("Inventory Updated for product...")
            
            elif event["event_type"] == "Product_Deleted":
                product = event["product"]
                delete_inventory(product["product_id"])
                print("Product deleted from inventory...")
    finally:
        await consumer.stop()






def add_inventory(product_id, Product_name , product_quantity):
    with Session(engine) as session:
        # inventory_item = session.query(Stock_update).filter(Stock_update.product_id == product_id).first()
        inventory_item = Stock_update(product_id=product_id, product_name=Product_name , product_quantity=product_quantity)
        session.add(inventory_item)
        session.commit()
        print("Product Added to Inventory...")


def update_inventory(product_id , product_name , product_quantity):
    with Session(engine) as session:
        inventory_item = session.query(Stock_update).filter(Stock_update.product_id == product_id).first()
        # if inventory_item:
        #     # inventory_item.product_name = product_name
        #     inventory_item = Stock_update(product_id=product_id, product_quantity=product_quantity)
        #     session.add(inventory_item)
        #     session.commit()
        #     session.refresh(inventory_item)
        if inventory_item:
            # Update existing fields
            inventory_item.product_name = product_name
            inventory_item.product_quantity = product_quantity
            session.commit()
            print("Product Updated in Inventory...")

        # inventory_item = session.query(Stock_update).filter(Stock_update.product_id == product_id).first()
        # if inventory_item:
        #     inventory_item = Stock_update(product_id=product_id, product_name=product_name, product_quantity=product_quantity)
        #     session.commit()
        #     print("Product Updated in Inventory...")


def delete_inventory(product_id):
    with Session(engine) as session:
        inventory_item = session.query(Stock_update).filter(Stock_update.product_id == product_id).first()
        if inventory_item:
            session.delete(inventory_item)
            session.commit()
            print("Product Deleted from Inventory...")



            ##### Notice the below code
            # data = msg.value
            # if data["event_type"] == "product_created":
            #     product_id = data["product_id"]
            #     stock = data["stock"]
            #     with Session(engine) as session:
            #         inventory_item = session.query(Stock_update).filter(Stock_update.product_id == product_id).first()
            #         if inventory_item:
            #             inventory = Stock_update(product_id=product_id, product_quantity=stock)
            #         else:
            #             inventory_item = Stock_update(
            #                 product_id=data["product_id"],
            #                 product_name=data["product_name"],
            #                 product_quantity=data.get("product_quantity", 0),
            #                 status=data.get("status", " In-stock")
            #             )

            #             session.add(inventory_item)
            #             print("Product Added to Inventory...")
            #             session.commit()
            # elif data["event_type"] == "product_updated":
            #     product_id = data["product_id"]
            #     stock = data["stock"]
            #     with Session(engine) as session:
            #         inventory_item = session.query(Stock_update).filter(Stock_update.product_id == product_id).first()
            #         if inventory_item:
            #             inventory_item.product_quantity = stock
            #             session.commit()
            # elif data["event_type"] == "product_deleted":
            #     product_id = data["product_id"]
            #     with Session(engine) as session:
            #         inventory_item = session.query(Stock_update).filter(Stock_update.product_id == product_id).first()
            #         if inventory_item:
            #             session.delete(inventory_item)
            #             session.commit()






    # while True:
    #     try:
    #         await consumer.start()
    #         logging.info("Consumer started...")                  
    #         async for msgs in consumer:
    #             data = json.loads(msgs.value.decode("utf-8"))
    #             if data["event_type"] == "product_created":
    #                 product_id = data["product_id"]
    #                 stock = data["stock"]
    #                 with Session(engine) as session:
    #                     inventory_item = session.query(Stock_update).filter(Stock_update.product_id == product_id).first()
    #                     if inventory_item:
    #                         inventory = Stock_update(product_id=product_id, product_quantity=stock)
    #                     else:
    #                         inventory_item = Stock_update(
    #                             product_id=data["product_id"],
    #                             product_name=data["product_name"],
    #                             product_quantity=data.get("product_quantity", 0),
    #                             status=data.get("status", " In-stock")
    #                         )

    #                         session.add(inventory_item)
    #                         print("Product Added to Inventory...")
    #                         session.commit()
                # logging.info(f"Consumer_messages...{data} ")
                # product_id = data.get("product_id")
                # if product_id is None:
                #     logging.info("Invalid data received, skipping...", data)
                #     continue 
                # with Session(engine) as session:
                #     inventory_item = session.query(Stock_update).filter(Stock_update.product_id == product_id).first()
                #     if inventory_item:
                #         inventory = Stock_update(product_id=product_id, product_name=prod)
                #     #     inventory_item.product_name = data.get("product_name", inventory_item.product_name)
                #     #     inventory_item.product_quantity = data.get("product_quantity", inventory_item.product_quantity)
                #     #     inventory_item.status = data.get("status", inventory_item.status)
                        
                #     # else:
                #     #     inventory_item = Stock_update(
                #     #         product_id=data["product_id"],
                #     #         product_name=data["product_name"],
                #     #         product_quantity=data.get("product_quantity", 0),
                #     #         status=data.get("status" , " In-stock")
                #     #     )

                #         session.add(inventory_item)
                    
                #     session.commit()
            
        # except KafkaConnectionError as e : 
        #     logging.info("Consumer starting failed, Retry in 5 sec...")
        #     await asyncio.sleep(5)
        
        # finally:
        #     await consumer.stop()

