from contextlib import asynccontextmanager
from typing import AsyncGenerator , Annotated  
from .database import create_db_and_tables ,engine , Order  , OrderResponse , get_db 
from sqlmodel import Session  , select
from aiokafka import AIOKafkaProducer
from .consumer import consume_messages
# from .consumer_for_inventory import inventory_cosnumer
from .producer import kafka_producer
import json , asyncio
# from .authenticate import verify_token     
# from fastapi.security import OAuth2PasswordRequestForm
from . import setting
from fastapi import FastAPI , HTTPException , Depends ,status
from .authenticate import verify_token
# from .utils import authenticate_user , Token
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm , OAuth2PasswordBearer


@asynccontextmanager 
async def lifespan(app : FastAPI)->AsyncGenerator[None,None]:
    print("Creating Tables...")
    task = asyncio.create_task(consume_messages())
    create_db_and_tables()
    yield

app : FastAPI = FastAPI(lifespan=lifespan , version="1.0.0")



# @app.post("/login" , response_model=create_user)
# async def login_user(login:Annotated[OAuth2PasswordRequestForm,Depends(OAuth2PasswordRequestForm)]):
#     create_user = User(
#         username = login.username,
#         # user_email = login.,
#         hashed_password = login.password
#     )
    


@app.post("/create_order" , response_model=OrderResponse)
async def create_order(order : Order , producer : Annotated[AIOKafkaProducer, Depends(kafka_producer)],
                       session : Annotated[Session, Depends(get_db)],
                        # verify_token : Annotated[User, Depends(verify_access_token)]
                        token_data : dict = Depends(verify_token),
                       ):
    user_id = token_data.get("sub")
    order.user_id = user_id
   
    statement = select(Order).where(Order.order_id == order.order_id)
    existing_order = session.exec(statement).first()
    # existing_order = session.query(Order).filter_by(id=order.order_id).first()
    if existing_order:
        raise HTTPException(status_code=400, detail="Order already exists")
    order_dict = {field : getattr(order, field) for field in order.dict()}
    order_json = json.dumps(order_dict).encode('utf-8')
    print("order_json", order_json)
    session.add(order)
    session.commit()
    session.refresh(order)
    try:
        event = {"event_type" : "Order_Created" , "order" : order.dict()}
        await producer.send_and_wait(setting.KAFKA_ORDER_TOPIC, json.dumps(event).encode('utf-8'))
        print("Order Details Send to kafka topic....")
    except Exception as e:
        print(f"Error Sending to Kafka {e}")
        session.rollback()
        raise HTTPException(status_code=500, detail="Error Sending order to kafka..")
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
    session.commit()
    session.refresh(db_order)
    try:    
        event = {"event_type" : "Order_Updated" , "order" : db_order.dict()}
        await producer.send_and_wait(setting.KAFKA_ORDER_TOPIC, json.dumps(event).encode('utf-8'))
        print("Updated Order Details Send to kafka topic....")
    except Exception as e:
        print(f"Error Sending to Kafka {e}")
    return db_order

######################################################################
@app.get("/get_order")
def get_order(db: Annotated[Session,Depends(get_db)],
            #   token : str = Depends(oauth2_scheme)
            #   , current_user : str = Depends(get_current_user)  
              ):
    # user_data = decode_access_token(token)
    # if user_data:
    order = db.exec(select(Order)).all()
    return order
    # return {"message" : "Order Fetched Successfully"}
    # else:
    # raise HTTPException(status_code=401, detail="Invalid token")

@app.get("/get_single_order")
def get_single_order(order_id : int , db : Annotated[Session , Depends(get_db)]):
    order = db.get(Order , order_id)
    if not order:
        raise HTTPException(status_code=404 , detail="order not found")
    return order



@app.delete("/delete_order")
async def delete_order(order_id : int , session : Annotated[Session , Depends(get_db)] ,
                 producer : Annotated[AIOKafkaProducer , Depends(kafka_producer)],
                #  current_user : str = Depends(get_current_user) 
                 ):
    order = session.get(Order, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="order not found")
    order_dict = {fields : getattr(order , fields) for fields in order.dict()}
    order_json = json.dumps(order_dict).encode("utf-8")
    print("Order_json" , order_json)
    session.delete(order)
    session.commit()
    try:
        event = {"event_type" : "Order_Deleted" , "order" : order.dict()}
        await producer.send_and_wait(setting.KAFKA_ORDER_TOPIC, json.dumps(event).encode('utf-8'))
        print("Order Details Send to kafka topic....")
    except Exception as e:
        print(f"Error Sending to Kafka {e}")
    return {"message" : "order deleted successfully"}