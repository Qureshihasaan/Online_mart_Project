from aiokafka import AIOKafkaConsumer
import logging
import asyncio
from aiokafka.errors import KafkaConnectionError
from ..email_services import send_email
from .. import setting
import json


loop = asyncio.get_event_loop()
logging.basicConfig(level=logging.INFO)

async def kafka_order_Created_consumer()-> AIOKafkaConsumer:
    consumer = AIOKafkaConsumer(
    setting.KAFKA_ORDER_CREATED_TOPIC,
    bootstrap_servers = setting.KAFKA_BOOTSTRAP_SERVER,
    group_id=setting.KAFKA_CONSUMER_GROUP_ID_FOR_NOTIFICATION_SERVICE,
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
            event = json.loads(msg.value.decode("utf-8"))
            print(type(event))
            print(f"Event Received: {event}")
            if event["event_type"] == "Order_Created":
                order_data= event.get("order", {})
                order_email =order_data.get("email")
                if not order_email:
                    logging.warning("Email not found in event. Skipping...")
                    continue
                subject = "Order Confirmation"
                body = (
                    "Your Order Has Been Created Successfully.\n\n"
                    "Best regards,\nThe Online Mart Team"
                )
                try:
                    await send_email(
                        to=event["email"],
                        subject="Order Confirmation",
                        body=f"Your Order Has Been Created Successfully.Best regards,\nThe Online Mart Team",
                )
                    logging.info(f"Order Confirmation email sent to {order_email}")
                except Exception as email_error:
                    logging.error(f"Failed to send order confirmation email to {order_email}: {email_error}")
    except json.JSONDecodeError as decode_error:
        logging.error(f"Failed to decode message: {msg.value}. Error: {decode_error}")

    except KeyError as key_error:
        logging.error(f"Missing key in event: {key_error}")
    finally:
        await consumer.stop()
        logging.info("Consumer Stopped...")


    # async def kafka_order_cancelled_consumer()-> AIOKafkaConsumer:
    #     consumer = AIOKafkaConsumer(
    #     setting.KAFKA_TOPIC_FOR_ORDER_CANCELLED,
    #     bootstrap_servers = setting.KAFKA_BOOTSTRAP_SERVER,
    #     group_id=setting.KAFKA_CONSUMER_GROUP_ID_FOR_ORDER_CANCELLED,
    #     auto_offset_reset="earliest",
    #     )
    #     while True:
    #         try:
    #             await consumer.start()
    #             logging.info("Consumer Started...")
    #             break
    #         except KafkaConnectionError as e:
    #             logging.info("Consumer Starting Failed, Retry in 5 sec...")
    #             await asyncio.sleep(5)

    #     try :
    #         async for msg in consumer:
    #             event = msg.value
    #             print("event", event)
    #             send_email(
    #                 to=event["email"],
    #                 subject="Order Cancelled",
    #                 body=f"Your Order Has Been Cancelled Successfully.Best regards,\nThe Online Mart Team",
    #             )

    #     finally:
    #         await consumer.stop()






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
