from fastapi import FastAPI , Depends , HTTPException
from typing import Annotated , AsyncGenerator , List
import asyncio
from contextlib import asynccontextmanager
from sqlmodel import Session , select
from .model import  Stock_update , Inventory_update
from .database import create_db_and_tables , engine
import json
from .conusmer import consume_message
from .producer import kafka_producer1
from aiokafka import AIOKafkaProducer
# from .event_consuming import consume_product_events
from . import setting

@asynccontextmanager
async def lifespan(app : FastAPI)->AsyncGenerator[None, None]:
    print("Tables Creating...")
    asyncio.create_task(consume_message())
    create_db_and_tables()
    yield 
            
            
            
app : FastAPI = FastAPI(lifespan=lifespan , version="1.0.0")


def get_db():
    with Session(engine) as session:
        yield session

@app.on_event("startup")
async def startup_event():
    consumer = await consume_message()
    asyncio.create_task((consumer()))
        


# @app.post("/stock_create" , response_model = Inventory_update)
# async def create_stock(product_stock_update : Stock_update , producer : Annotated[AIOKafkaProducer , Depends(kafka_producer1)] ,
#                        session : Annotated[Session , Depends(get_db)]
#                        )-> Stock_update:
#     product_dict = {field : getattr(product_stock_update , field) for field in product_stock_update.dict()}
#     product_json = json.dumps(product_dict).encode("utf-8")
#     print("Product_json" , product_json)
#     await producer.send_and_wait(setting.KAFKA_PRODUCT_TOPIC , product_json)
#     session.add(product_stock_update)
#     session.commit()
#     session.refresh(product_stock_update)
#     return product_stock_update


@app.put("/stock_update{stock_id}" , response_model=Inventory_update)
async def stock_update(stock_id : int , item_stock_update : Stock_update , db : Annotated[Session , Depends(get_db)],
                 producer : Annotated[AIOKafkaProducer , Depends(kafka_producer1)]
                 ):
    stock = db.get(item_stock_update, stock_id)
    if not stock:
        raise HTTPException(status_code=404, detail="Stock not found")
    stock_dict = {field : getattr(item_stock_update, field) for field in item_stock_update.dict()}
    stock_json = json.dumps(stock_dict).encode("utf-8")
    print("stock_json", stock_json)
    await producer.send_and_wait(setting.KAFKA_PRODUCT_TOPIC, stock_json)
    db.commit()
    db.refresh(stock)
    return stock
        
        
@app.get("/get_single_stock_update")
def get_single_stock_update(stock_id : int, db : Annotated[Session, Depends(get_db)]):
    stock = db.get(Stock_update, stock_id)
    if not stock:
        raise HTTPException(status_code=404, detail="Stock not found")
    return stock        
        


@app.get("/get_stock_update")
def get_stock_update(db : Annotated[Session, Depends(get_db)]):
    stock = db.exec(select(Stock_update)).all()
    return stock

@app.delete("/stock_delete{stock_id}")
async def delete_stock(stock_id : int , session : Annotated[Session , Depends(get_db)],
                       producer : Annotated[AIOKafkaProducer, Depends(kafka_producer1)]
                       ):
    db_product = session.get(Stock_update, stock_id)
    if not db_product:
        raise HTTPException(status_code=404, detail = "Product Not Found")
    product_dict = {
         "event_type" : "stock_deleted",
          "stock_id" : stock_id
         }
    product_json = json.dumps(product_dict).encode("utf-8")
    print("product_json" , product_json)
    await producer.send_and_wait(setting.KAFKA_PRODUCT_TOPIC
                                 , db_product)
    session.delete(db_product)
    session.commit()
    return db_product

# @app.put("/stock_update/{stock_id}" , response_model = stock_update)
# async def update_stock(stock_id : int , item_stock_update : stock_update,
#                        producer : Annotated = [AIOKafkaProducer , Depends(kafka_producer1)],
#                        db: Session = Depends(get_db)
#                        ):
#     stock = db.get(item_stock_update , stock_id)
#     if not stock:
#         raise HTTPException(status_code=404, detail="Stock not found")
#     stock_dict = {field : getattr(item_stock_update, field) for field in item_stock_update.dict()}
#     stock_json = json.dumps(stock_dict).encode("utf-8")
#     print("stock_json" , stock_json)
#     await producer.send_and_wait("my_topic1", stock_json)
#     db.commit()
#     db.refresh(stock)
#     return stock


# @app.put("/stock_update/{stock_id}" , response_model= Inventory_update)
# async def update_stock(stock_id : int , it)


# @app.delete("/stock_delete{stock_id}")
# def delete_stock(id : int , session : Annotated[Session , Depends(get_db)],
                 
#                  ):
#     db_product = session.get(stock_update, id)
#     if not db_product:
#         raise HTTPException(status_code=404, details = "Product Not Found")
#     product_dict = {fields : getattr(db_product , fields) for fields in db_product.dict()}
#     product_json = json.dumps(product_dict).encode("utf-8")
#     print("product_json" , product_json)
#     session.delete(db_product)
#     session.commit()
#     return db_product