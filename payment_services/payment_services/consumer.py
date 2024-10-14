import asyncio
import logging
from aiokafka import AIOKafkaConsumer
from aiokafka.errors import KafkaConnectionError


loop = asyncio.get_event_loop()
logging.basicConfig(level=logging.INFO)


async def consume_messages(topic , bootstarpserver)->AIOKafkaConsumer:
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=bootstarpserver,
        group_id="my-group",
        auto_offset_reset="earliest"
    )

    while True:
        try:
            await consumer.start()
            logging.info("consumer started...")
            break
        except KafkaConnectionError as e:
            logging.info("Consumer starting failed, Retry in 5 sec...")
            await asyncio.sleep(5)

    try:
        async for messages in consumer:
            consume = messages.value
            print("Consumer_messages" , consume)
    except:
        await consumer.stop()