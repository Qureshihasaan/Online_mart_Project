from contextlib import asynccontextmanager
from typing import  AsyncGenerator
from fastapi import  FastAPI
from sqlmodel import  Session
from .database import create_db_and_tables , engine
# import asyncio
# from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
# import json
# from .setting import BOOT_STRAP_SERVER, KAFKA_ORDER_TOPIC
# from datetime import datetime
from .send_email import send_email

# async def send_email(user_id , message):
#     print(f"Sending Email to User {user_id}: {message}")


# async def send_sms(user_id , message):
#     print(f"Sendinfg Message to User {user_id}: {message}")



# loop = asyncio.get_event_loop()
# logging.basicConfig(level=logging.INFO)

# async def consume_notifications():
#     consumer = AIOKafkaConsumer(
#         KAFKA_ORDER_TOPIC,
#         bootstrap_servers=BOOT_STRAP_SERVER,
#         group_id="my-group",
#         auto_offset_reset="earliest"
#     )

#     await consumer.start()
#     try: 
#         async for msg in consumer:
#             notification = json.loads(msg.value)
#             user_id = notification["user_id"]
#             notification_type = notification["notification_type"]
#             message = notification["message"]

#             with Session(engine) as session:
#                 user_pref = session.exec(select(notification_preference).where(notification_preference.user_id==user_id)).first()

#                 if not user_pref:
#                     print(f"No user Preference found with {user_id}")
#                     continue

#                 if user_pref.email_notification:
#                     await send_email(user_id , message)

#                 if user_pref.sms_notification:
#                     await send_sms(user_id , message)

# #     finally:
#         await consumer.stop()



@asynccontextmanager
async def lifespan(app : FastAPI)->AsyncGenerator[None,None]:
    create_db_and_tables()
    yield


app : FastAPI = FastAPI(lifespan=lifespan , version="1.0.0")



def get_db():
    with Session(engine) as session:
        yield session


# async def kafka_producer():
#     producer = AIOKafkaProducer(bootstrap_servers=str("broker:19092"))
#     await producer.start()
#     return producer

# async def send_notification_event(user_id : int , notification_type : str , message : str):
#     producer = await kafka_producer()
#     notification = {
#         "user_id" : user_id,
#         "notification_type" : notification_type,
#         "message" : message,
#         "timestamp" : datetime.utcnow().isoformat(),
#     }
#     await producer.send_and_wait(KAFKA_ORDER_TOPIC , json.dumps(notification).encode("utf-8"))
#     await producer.stop()



# # @app.post("/signup")
# # async def signup_notify(user_id : int , session : Annotated[Session, Depends(get_db)]):
# #     message = "Thanks For Using Our Services And For SigningUp!"
# #     await send_notification_event(user_id , "sign_up" , message)
# #     return {"message" : "SignUp Notification Sent..."}


# # @app.post("/Login")
# # async def login_notify(user_id : int , session : Annotated[Session, Depends(get_db)]):
# #     message = "You Have Successfully Logged In..."
# #     await send_notification_event(user_id , "Login" , message)
# #     return{"messge" : "Login Notification Sent..."}


# # @app.post("/order_status")
# # async def order_status(user_id : int , status : str , session : Annotated[Session,Depends(get_db)]):
# #     message = f"Your Order Status Has Been Updated To: {status}"
# #     await send_notification_event(user_id , "order_status" , message)
# #     return {"message" : "Order Status Notification Sent"}

# # @app.post("/delivery_update")
# # async def delivery_notify(user_id : int , delivery_status : str , session : Annotated[Session, Depends(get_db)]):
# #     message = f"Your Delivery Status: {delivery_status}"
# #     await send_notification_event(user_id , "Delivery" , message)
# #     return {"message" : "Delivery Notification Sent..."}


@app.post("/send_notification")
async def send_notification(to_email : str , subject : str , message : str):
    send_email(to_email, subject, message)
    return {"message" : "Email Sent Successfully..."}