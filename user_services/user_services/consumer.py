from aiokafka import AIOKafkaConsumer
import logging
from aiokafka.errors import KafkaConnectionError
import asyncio


loop = asyncio.get_event_loop()
logging.basicConfig(level=logging.INFO)

async def consume(topic , bootstrapserver)->AIOKafkaConsumer:
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=bootstrapserver,
        group_id="user_service_group",
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
          
