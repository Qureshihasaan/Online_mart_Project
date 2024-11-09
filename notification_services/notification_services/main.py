from contextlib import asynccontextmanager
from typing import  AsyncGenerator
from fastapi import  FastAPI
from sqlmodel import  Session
from .database import engine
from .send_email import send_email
import asyncio , logging
from .Consumer import kafka_order_consumer , kafka_payment_consumer , kafka_user_consumer

loop = asyncio.get_event_loop()
logging.basicConfig(level=logging.INFO)




@asynccontextmanager
async def lifespan(app : FastAPI)->AsyncGenerator[None,None]:
   loop = asyncio.get_event_loop()
   task1 = loop.create_task(kafka_user_consumer.New_user_created_consumer())
   task2 = loop.create_task(kafka_order_consumer.kafka_order_Created_consumer())
   task3 = loop.create_task(kafka_payment_consumer.kafka_payment_consumer())
   
   
   try:
       yield
   finally:
       for task in [task1, task2, task3]:
           task.cancel()
           try:
               await task
           except asyncio.CancelledError:
               pass



app : FastAPI = FastAPI(lifespan=lifespan , version="1.0.0")



def get_db():
    with Session(engine) as session:
        yield session




@app.get("/")
def get_root():
    return{"message" : "Welcome To Notification Service..."}

# @app.on_event("startup")
# async def startup_event():
#     asyncio.create_task(kafka_consumer())


# async def kafka_producer():
#     producer = AIOKafkaProducer(bootstrap_servers=str("broker:19092"))
#     await producer.start()
#     return producer


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


# @app.post("/send_notification")
# async def send_notification(to_email : str , subject : str , message : str):
#     send_email(to_email, subject, message)
#     return {"message" : "Email Sent Successfully..."}

