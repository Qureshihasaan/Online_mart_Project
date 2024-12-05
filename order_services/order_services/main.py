from contextlib import asynccontextmanager
from typing import AsyncGenerator , Annotated  
from .database import create_db_and_tables ,engine , Order  , OrderResponse , get_db
from sqlmodel import Session  , select
from aiokafka import AIOKafkaProducer
from .consumer import consume_messages
from .producer import kafka_producer
import json , asyncio
# from .authenticate import verify_token     
# from fastapi.security import OAuth2PasswordRequestForm
from . import setting
from fastapi import FastAPI , HTTPException , Depends ,status
# from .authenticate import decode_access_token , ACCESS_TOKEN_EXPIRE_MINUTES , create_access_token
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


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

# INVENTORY_SERVICE_URL = "http://inventory-services:8001"



# @app.post("/login" , response_model=Token)
# async def login_with_token(# form_data : Annotated[OAuth2PasswordRequestForm,Depends()],
#                             user_name : str , password : str ,
#                            db : Annotated[Session, Depends(get_db)]
#                            )->Token:
#     user = authenticate_user(user_name, password, db)
#     if not user:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could Not Validate User")
#     access_token = create_access_token(user.username , user.id , timedelta(minutes= ACCESS_TOKEN_EXPIRE_MINUTES))
#     return {"access_token" : access_token, "token_type" : "bearer"}



@app.post("/create_order" , response_model=OrderResponse)
async def create_order(order : Order , producer : Annotated[AIOKafkaProducer, Depends(kafka_producer)],
                       session : Annotated[Session, Depends(get_db)],
                        # token:  Annotated[str ,Depends(oauth2_scheme)]
                       # token: Annotated[str , Depends(oauth2_scheme)] 
                       ):
    # user_token_data = decode_access_token(token)
    # user_data = decode_access_token(token)
    # user_id = user_data["id"]
    
    # user_email = session.get(user_id , {}).get("email")
    # user_id = current_user.get("user_id")
    # user_email = current_user.get("user_email")
    # if user_id is None or user_email is None:
    #     raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    statement = select(Order).where(Order.order_id == order.order_id)
    existing_order = session.exec(statement).first()
    # existing_order = session.query(Order).filter_by(id=order.order_id).first()
    if existing_order:
        raise HTTPException(status_code=400, detail="Order already exists")
    # try:
    #     inventory_response = requests.get(
    #         f"{INVENTORY_SERVICE_URL}/check_inventory",
    #         params={"product_id": order.product_id, "quantity": order.product_quantity}
    #     )
    #     inventory_status = inventory_response.json()
    #     if not inventory_status.get("available"):
    #         raise HTTPException(status_code=400, detail="Product not available in inventory")
    # except requests.RequestException as e:
    #     print(f"Error Communicating with inventory service: {e}")
    #     raise HTTPException(status_code=500, detail="Error checking inventory")
    order_dict = {field : getattr(order, field) for field in order.dict()}
    order_json = json.dumps(order_dict).encode('utf-8')
    print("order_json", order_json)
    # try:
    #     Event = {"event_type" : "Checking_Inventory" , "order" : {"product_id" : order.product_id , "quantity" : order.product_quantity}}
    #     await producer.send_and_wait(setting.KAFKA_ORDER_TOPIC , json.dumps(Event).encode("utf-8"))
    #     print("Order Details Send to Kafka Topic for Inventory Checking...")
    # except Exception as e:
    #     print(f"Error Sending to Kafka {e}")
    #     raise HTTPException(status_code=500, detail="Error Sending order to kafka..")
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