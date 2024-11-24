import asyncio , logging
from aiokafka import AIOKafkaConsumer
from aiokafka.errors import KafkaConnectionError
from . import setting

loop = asyncio.get_event_loop()
logging.basicConfig(level=logging.INFO)

async def consume_messages() ->AIOKafkaConsumer:
    consumer = AIOKafkaConsumer(
        setting.KAFKA_ORDER_TOPIC,
        bootstrap_servers= setting.BOOT_STRAP_SERVER,
        group_id =setting.KAFKA_CONSUMER_GROUP_ID_FOR_ORDER,
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



# async def consume_messages_from_user_to_order():
#     consumer = AIOKafkaConsumer(
#         setting.KAFKA_TOPIC_FROM_USER_TO_ORDER,
#         bootstrap_servers= setting.BOOT_STRAP_SERVER,
#         group_id = "my_group",
#         auto_offset_reset = "earliest"
#     )

#     while True:
#         try:
#             await consumer.start()
#             logging.info("Consumer Started....")
#             break
#         except KafkaConnectionError as e:
#             logging.info("Consumer starting failed, Retry in 5 seconds...")

#     try:
#         async for messages in consumer:
#             consume = messages.value
#             print("consumer_messages", consume)
#     finally:
#         await consumer.stop()
