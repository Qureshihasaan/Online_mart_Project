import asyncio, logging , json
from aiokafka import AIOKafkaConsumer
from aiokafka.errors import KafkaConnectionError



loop = asyncio.get_event_loop()
logging.basicConfig(level=logging.INFO)


async def consume_message(topic , bootstrapserver):
    consumer = AIOKafkaConsumer(
        topic, 
        bootstrap_servers=bootstrapserver,
        group_id="inventory_service_group",
        auto_offset_reset="earliest",
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )
    
    while True:
        try:
            await consumer.start()
            logging.info("Consumer started...")
        except KafkaConnectionError as e : 
            logging.info("Consumer starting failed, Retry in 5 sec...")
            await asyncio.sleep(5)
            
            
        try:
            async for messages in consumer:
                consume = messages.value
                print("Consumer_messages " ,consume)    
        finally:
            await consumer.stop()