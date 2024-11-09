from aiokafka import AIOKafkaConsumer
import logging
from aiokafka.errors import KafkaConnectionError
import asyncio
from . import setting

loop = asyncio.get_event_loop()
logging.basicConfig(level=logging.INFO)

async def consume()->AIOKafkaConsumer:
    consumer = AIOKafkaConsumer(
        setting.KAFKA_USER_TOPIC,
        bootstrap_servers=setting.BOOTSTRAP_SERVER,
        group_id=setting.KAFKA_CONSUMER_GROUP_ID_FOR_USER,
        auto_offset_reset="earliest"
        )
    while True:
        try :
            await consumer.start()
            logging.info("Consumer Started...")
            break
        except KafkaConnectionError as e: 
            logging.info("Consumer staring failed, Retry in 5 sec")
            await asyncio.sleep(5)
                   
                   
    try: 
        async for messages in consumer:
            consume = messages.value
            print("consumer_messages " , consume )
    finally:
        await consumer.stop()
          
