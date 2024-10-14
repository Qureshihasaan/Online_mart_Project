from fastapi import FastAPI , HTTPException , Depends
from contextlib import asynccontextmanager
from typing import AsyncGenerator , Annotated
from .database import create_db_and_tables ,engine , Order
from sqlmodel import Session  , select
import asyncio , logging
from aiokafka import AIOKafkaConsumer , AIOKafkaProducer
from aiokafka.errors import KafkaConnectionError
import json

# PRODUCT_SERVICE_URL = "http://localhost:8000/docs"

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



@asynccontextmanager 
async def lifespan(app : FastAPI)->AsyncGenerator[None,None]:
    print("Creating Tables...")
    task = asyncio.create_task(consume_messages("my_topic2" , "broker:19092"))
    create_db_and_tables()    
    yield


app : FastAPI = FastAPI(lifespan=lifespan , version="1.0.0")

def get_db():
    with Session(engine) as session:
        yield Session


async def kafka_producer():
    producer = AIOKafkaProducer(bootstrap_servers = str("broker:19092"))
    await producer.start()
    try: 
        yield producer
    finally:
        await producer.stop()


@app.post("/create_order")
async def create_order(order : Order , producer : Annotated[AIOKafkaProducer , Depends(kafka_producer)] ,
    db : Annotated[Session , Depends(get_db)]):
    order_dict = {field : getattr(order, field) for field in order.dict()}
    order_json = json.dumps(order_dict).encode("utf-8")
    print("order_json" , order_json)
    await producer.send_and_wait("my_topic" , order_json)
    # existing_order = db.query(Order).filter_by(order_id=order.order_id).first()
    statement = select(Order).where(Order.order_id == order.order_id)
    existing_order = db.exec(statement).first()
    if existing_order:
        raise HTTPException(status_code = 400 , detail = "order already exists")
    db.add(order)
    db.commit()
    db.refresh(order)
    return order


@app.get("/get_order")
def get_order(db: Annotated[Session,Depends(get_db)]):
    order = db.exec(select(Order)).all()
    return order

@app.get("/get_single_order")
def get_single_order(order_id : int , db : Annotated[Session , Depends(get_db)]):
    order = db.get(Order , order_id)
    if not order:
        raise HTTPException(status_code=404 , detail="order not found")
    return order



@app.delete("/delete_order")
def delete_order(order_id : int , session : Annotated[Session , Depends(get_db)] ,
                 producer : Annotated[AIOKafkaProducer , Depends(kafka_producer)]):
    order = session.get(Order, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="order not found")
    order_dict = {fields : getattr(order , fields) for fields in order.dict()}
    order_json = json.dumps(order_dict).encode("utf-8")
    print("Order_json" , order_json)
    producer.send_and_wait("my_topic", order)
    session.delete(order)
    session.commit()
    return {"message" : "order deleted successfully"}