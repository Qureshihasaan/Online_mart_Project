from fastapi import FastAPI , HTTPException , Depends , status
from contextlib import asynccontextmanager
from typing import AsyncGenerator , Annotated  
from .database import create_db_and_tables ,engine , Order , Order_request
from sqlmodel import Session  , select
from aiokafka import AIOKafkaProducer
from .consumer import consume_messages
from .producer import kafka_producer
import json , asyncio
from .authenticate import verify_token     
from fastapi.security import OAuth2PasswordRequestForm
from . import setting



@asynccontextmanager 
async def lifespan(app : FastAPI)->AsyncGenerator[None,None]:
    print("Creating Tables...")
    task = asyncio.create_task(consume_messages(
        setting.KAFKA_ORDER_TOPIC , bootstrap_servers=str("broker:19092")))
    if task:
        print("Consuming Messages.....")
    create_db_and_tables()    
    yield


app : FastAPI = FastAPI(lifespan=lifespan , version="1.0.0")

def get_db():
    with Session(engine) as session:
        yield Session

@app.post("/create_order" , response_model=Order_request)
async def create_order(order : Order , producer : Annotated[AIOKafkaProducer, Depends(kafka_producer)],
                       session : Annotated[Session, Depends(get_db)]
                       ):
    order_dict = {fields : getattr(order, fields) for fields in order.dict()}
    order_json = json.dumps(order_dict).encode('utf-8')
    print("order_json", order_json)
    session.add(order_json)
    session.commit()
    session.refresh(order_json )
    event = {"event_type" : "Order_Created" , "order" : order.dict}
    await producer.send_and_wait(setting.KAFKA_ORDER_TOPIC, json.dumps(event).encode("utf-8"))
    return order

@app.put("/update_order{order_id}")
async def update_order(order_id : int , update_order : Order , producer : Annotated[AIOKafkaProducer, Depends(kafka_producer)],
                       session : Annotated[Session, Depends(get_db)]                       
                       ):
    db_order = session.get(Order , order_id)
    if not db_order:
        raise HTTPException(status_code=404 , detail=f"Order With this {order_id} not found")    
    order_dict = {fields : getattr(db_order ,fields) for fields in db_order.dict()}
    order_json = json.dumps(order_dict).encode('utf-8')
    print("order_json" , order_json)
    await producer.send_and_wait("order_topic", order_json)
    session.commit()
    session.refresh(db_order)
    return db_order


@app.get("/get_order")
def get_order(db: Annotated[Session,Depends(get_db)]
            #   , current_user : str = Depends(get_current_user)  
              ):
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
                 producer : Annotated[AIOKafkaProducer , Depends(kafka_producer)],
                #  current_user : str = Depends(get_current_user) 
                 ):
    order = session.get(Order, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="order not found")
    order_dict = {fields : getattr(order , fields) for fields in order.dict()}
    order_json = json.dumps(order_dict).encode("utf-8")
    print("Order_json" , order_json)
    producer.send_and_wait("order_topic", order)
    session.delete(order)
    session.commit()
    return {"message" : "order deleted successfully"}