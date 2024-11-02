import asyncio , logging
from aiokafka import AIOKafkaConsumer
from aiokafka.errors import KafkaConnectionError


loop = asyncio.get_event_loop()
logging.basicConfig(level=logging.INFO)

async def consume_messages(topic , bootstrap_servers) ->AIOKafkaConsumer:
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers= bootstrap_servers,
        group_id = "my_group",
        auto_offset_reset = "earliest"
    )


    while True:
        try:
            await consumer.start()
            logging.info("Consumer Started....")
            break
        except KafkaConnectionError as e:
            logging.info("Consumer starting failed , Retry in 5 seconds...")
            await asyncio.sleep(5)

    try:
        async for messages in consumer:
            consume = messages.value
            print("consumer_messages" , consume)
    finally:
        await consumer.stop()