from aiokafka import AIOKafkaConsumer
import asyncio , logging 
from .. import setting
from aiokafka.errors import KafkaConnectionError    
from .. import send_email

loop = asyncio.get_event_loop()
logging.basicConfig(level=logging.INFO)


async def kafka_payment_consumer()->AIOKafkaConsumer:
    consumer = AIOKafkaConsumer(
    setting.KAFKA_TOPIC_FOR_PAYMENT_DONE,
    bootstrap_servers=setting.KAFKA_BOOTSTRAP_SERVER,
    group_id=setting.KAFKA_CONSUMER_GROUP_ID_FOR_PAYMENT_DONE,
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
                subject="Payment Done",
                body=f"Your Payment Has Been Done Successfully.Best regards,\nThe Online Mart Team",
            )
    
    finally:
        await consumer.stop()