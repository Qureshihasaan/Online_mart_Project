from aiokafka import AIOKafkaConsumer , AIOKafkaProducer
import asyncio , logging , json
from . import setting
from sqlmodel import Session
from .database import engine
from .model import Stock_update


loop = asyncio.get_event_loop()
logging.basicConfig(level=logging.INFO)



async def inventory_checking_consumer():
    consumer = AIOKafkaConsumer(
        setting.KAFKA_ORDER_TOPIC,
        bootstrap_servers=setting.BOOTSTRAP_SERVER,
        group_id=setting.KAFKA_CONSUMER_GROUP_ID_FOR_INVENTORY,
        auto_offset_reset="earliest",
        value_deserializer=lambda x: json.loads(x.decode("utf-8"))
    )
    await consumer.start()
    logging.info("Consumer started...")
    
    try:
        async for msg in consumer:
            event = json.loads(msg.value.decode("utf-8"))
            logging.info(f"Event received: {event}")
            availability_status = await check_stock_availability(event)

    finally:
        await consumer.stop()
        logging.info("Consumer stopped.")


producer = AIOKafkaProducer(bootstrap_servers="localhost:9092") 



async def check_stock_availability(event_data : dict):
    product_id = event_data["product_id"]
    product_quantity = event_data["product_quantity"]
    order_id = event_data["order_id"]
    with Session(engine) as session:
        inventory_item = session.query(Stock_update).filter(Stock_update.product_id == product_id).first()
        if not inventory_item or inventory_item.product_quantity < product_quantity:
            status = {"order_id" : order_id , "status" : "Out of Stock"}
        else:
            inventory_item.prduct_quantity -= product_quantity
            session.add(inventory_item)
            session.commit()
            status = {"order_id" : order_id , "status" : "In Stock"}

        await producer.send_and_wait(topic=setting.KAFKA_ORDER_TOPIC , value=json.dumps(status).encode("utf-8"))