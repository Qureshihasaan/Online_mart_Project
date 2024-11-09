from aiokafka import AIOKafkaConsumer
import logging , asyncio
from .. import setting
from aiokafka.errors import KafkaConnectionError
from .. import send_email

loop = asyncio.get_event_loop()
logging.basicConfig(level=logging.INFO)


async def New_user_created_consumer()-> AIOKafkaConsumer:
    consumer = AIOKafkaConsumer(
        setting.KAFKA_TOPIC_FOR_NEW_USER,
        bootstrap_servers=setting.KAFKA_BOOTSTRAP_SERVER,
        group_id=setting.KAFKA_CONSUMER_GROUP_ID_FOR_NEW_USER,
        auto_offset_reset="earliest"
    )
    
    while True:
        try :
            await consumer.start()
            logging.info("Consumer Started...")
            break
        except KafkaConnectionError as e:
            logging.info("Consumer Starting Failed, Retry in 5 sec...")
            await asyncio.sleep(5)

    try:
        async for msg in consumer:
            event = msg.value
            print("event", event)
            send_email(
                to=event["email"],
                subject="Welcome to Online Mart",
                body=f"Welcome to Online Mart! Thank you for joining us. We're excited to have you on board. Best regards, The Online Mart Team",
            )

    finally:
        await consumer.stop()