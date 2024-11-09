import asyncio, logging 
from aiokafka import AIOKafkaConsumer
from aiokafka.errors import KafkaConnectionError
from . import setting
from .database import engine
from sqlmodel import Session
from .model import Stock_update
import json


loop = asyncio.get_event_loop()
logging.basicConfig(level=logging.INFO)


async def consume_message():
    consumer = AIOKafkaConsumer(
        setting.KAFKA_PRODUCT_TOPIC,
        bootstrap_servers=setting.BOOTSTRAP_SERVER,
        group_id=setting.KAFKA_CONSUMER_GROUP_ID_FOR_INVENTORY,
        auto_offset_reset="earliest",
    
    )
    
    while True:
        try:
            await consumer.start()
            logging.info("Consumer started...")                  
            async for msgs in consumer:
                data = json.loads(msgs.value.decode("utf-8"))
                logging.info(f"Consumer_messages...{data} ")
                product_id = data.get("product_id")
                if product_id is None:
                    logging.info("Invalid data received, skipping...", data)
                    continue 
                with Session(engine) as session:
                    inventory_item = session.query(Stock_update).filter(Stock_update.product_id == product_id).first()
                    if inventory_item:
                        inventory_item.product_name = data.get("product_name", inventory_item.product_name)
                        inventory_item.product_quantity = data.get("product_quantity", inventory_item.product_quantity)
                        inventory_item.status = data.get("status", inventory_item.status)
                        
                    else:
                        inventory_item = Stock_update(
                            product_id=data["product_id"],
                            product_name=data["product_name"],
                            product_quantity=data.get("product_quantity", 0),
                            status=data.get("status" , " In-stock")
                        )

                        session.add(inventory_item)
                    
                    session.commit()
            
        except KafkaConnectionError as e : 
            logging.info("Consumer starting failed, Retry in 5 sec...")
            await asyncio.sleep(5)
        
        finally:
            await consumer.stop()