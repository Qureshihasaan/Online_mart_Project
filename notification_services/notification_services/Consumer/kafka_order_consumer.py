from aiokafka import AIOKafkaConsumer
import logging
import asyncio
from aiokafka.errors import KafkaConnectionError
from ..send_email import send_email
from .. import setting


loop = asyncio.get_event_loop()
logging.basicConfig(level=logging.INFO)

async def kafka_order_Created_consumer()-> AIOKafkaConsumer:
    consumer = AIOKafkaConsumer(
    setting.KAFKA_TOPIC_FOR_ORDER_CREATED,
    bootstrap_servers = setting.KAFKA_BOOTSTRAP_SERVER,
    group_id=setting.KAFKA_CONSUMER_GROUP_ID_FOR_ORDER_CREATED,
    auto_offset_reset="earliest",
    )
    while True:
        try:
            await consumer.start()
            logging.info("Consumer Started...")
            break
        except KafkaConnectionError as e:
            logging.info("Consumer Starting Failed, Retry in 5 sec...")
            await asyncio.sleep(5)

    try :
        async for msg in consumer:
            event = msg.value
            print("event", event)
            send_email(
                to=event["email"],
                subject="Order Confirmation",
                body=f"Your Order Has Been Created Successfully.Best regards,\nThe Online Mart Team",
            )

    finally:
        await consumer.stop()


    async def kafka_order_cancelled_consumer()-> AIOKafkaConsumer:
        consumer = AIOKafkaConsumer(
        setting.KAFKA_TOPIC_FOR_ORDER_CANCELLED,
        bootstrap_servers = setting.KAFKA_BOOTSTRAP_SERVER,
        group_id=setting.KAFKA_CONSUMER_GROUP_ID_FOR_ORDER_CANCELLED,
        auto_offset_reset="earliest",
        )
        while True:
            try:
                await consumer.start()
                logging.info("Consumer Started...")
                break
            except KafkaConnectionError as e:
                logging.info("Consumer Starting Failed, Retry in 5 sec...")
                await asyncio.sleep(5)

        try :
            async for msg in consumer:
                event = msg.value
                print("event", event)
                send_email(
                    to=event["email"],
                    subject="Order Cancelled",
                    body=f"Your Order Has Been Cancelled Successfully.Best regards,\nThe Online Mart Team",
                )

        finally:
            await consumer.stop()






# async def kafka_consumer( , bootstrapserver)->AIOKafkaConsumer:
#     consumer = AIOKafkaConsumer(
#         bootstrap_servers=bootstrapserver,
#         group_id="my-group",
#         auto_offset_reset="earliest"
#     )
#     while True:
#         try:
            
#             await consumer.start()
#             logging.info("Consumer Started...")
#             break
#         except KafkaConnectionError as e:
#             logging.info("Consumer Starting Failed, Retry in 5 sec...")
#             await asyncio.sleep(5)
    
#     try: 
#         async for messages in consumer:
#             consume = messages.value
#             print("consumer_value" , consume)

#     finally:
#         await consumer.stop()
