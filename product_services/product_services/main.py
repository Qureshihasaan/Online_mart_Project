from fastapi import FastAPI , Depends , HTTPException
from aiokafka import AIOKafkaProducer
from contextlib import asynccontextmanager
from .consumer import consume_messages
from .producer import kafka_producer    
import asyncio
from typing import AsyncGenerator , Annotated
from .database import Product , Session , engine , create_db_and_tables
import json
from sqlmodel import select
from . import setting
from itertools import product


     
@asynccontextmanager
async def lifespan(app : FastAPI) -> AsyncGenerator[None , None]:
     print("Tables Creating")
     task = asyncio.create_task(consume_messages(setting.KAFKA_PRODUCT_TOPIC , setting.BOOTSTRAP_SERVER))
     create_db_and_tables()
     yield 



app : FastAPI = FastAPI(lifespan=lifespan , version="1.0.0")


def get_db():
    with Session(engine) as session:
        yield session



              
              
              
@app.post("/product" , response_model = Product)
async def product_service(product : Product , producer : Annotated[AIOKafkaProducer , Depends(kafka_producer)],
                          session : Annotated[Session , Depends(get_db)]
                          )->Product:
    # product_dict = {field : getattr(product, field) for field in product.dict()}
    # product_json = json.dumps(product_dict).encode("utf-8")
    # print("product_json", product_json)
    # # product_dict = product.dict()
    # # print("product_dict" , product_dict)
    # try: 
    #     session.add(product)
    #     session.commit()
    #     session.refresh(product) 
    # except Exception as e:
    #     print("Error:", e)
    #     raise HTTPException(status_code=500, detail="Internal Server Error")
    # event = {"event_type" : "Product_Created" , "product" : product.dict()}
    # try:
    #     await producer.send_and_wait(setting.KAFKA_PRODUCT_TOPIC  ,json.dumps(event).encode("utf-8")) #producer
    # except Exception as kafka_error:
    #     print("Kafka Error:", kafka_error)
    #     raise HTTPException(status_code=500, detail="Kafka Error")
    # print("Product Send to Kafka topic")
    # return product
    product_dict = {field : getattr(product, field) for field in product.dict()}
    product_json = json.dumps(product_dict).encode("utf-8")
    print("Product_json" , product_json)
    session.add(product)
    session.commit()
    session.refresh(product) 
    try:
        event = {"event_type" : "Product_Created" , "product" : product.dict()}
        await producer.send_and_wait(setting.KAFKA_PRODUCT_TOPIC ,  json.dumps(event).encode("utf-8")) #producer
        print("Product Send to Kafka topic")
    except Exception as e:
        print("Error Sending to Kafka", e)
    return product




@app.get("/product/" , response_model=list[Product])
async def get_product(session : Annotated[Session , Depends(get_db)]):
     products = session.exec(select(Product)).all()
     return  products


@app.put("/product/{product_id}" , response_model= Product)
async def update_product(product_id : int , product : Product , 
                         producer : Annotated[AIOKafkaProducer, Depends(kafka_producer)],
                         session : Annotated[Session , Depends(get_db)]):
    db_product = session.get(Product , product_id)
    if not db_product:
        raise HTTPException(status_code=404 , detail = "Product Not Found")
    
    for fields , value in product.dict(exclude_unset=True).items():
        setattr(db_product , fields, value)
        
    product_dict = {fields : getattr(db_product , fields) for fields in db_product.dict()}
    product_json = json.dumps(product_dict).encode("utf-8")
    print("product_json" , product_json)
    session.commit()
    session.refresh(db_product)
    try:
        event = {"event_type" : "Product_Updated" , "product" : product.dict()}
        await producer.send_and_wait(setting.KAFKA_PRODUCT_TOPIC , json.dumps(event).encode("utf-8"))
        print("Updated_Product Send to Kafka topic")
    except Exception as e:
        print("Error Sending to Kafka", e)  
    return db_product

    #  db_product = session.get(Product , product_id)
    #  if not db_product:
    #     raise HTTPException(status_code=404 , detail = "Product Not Found")
    
    #  # for fields , value in product.dict(exclude_unset=True).items():
    #  #    setattr(db_product , fields, value)
        
    #  product_dict = {
    #      "event_type" : "product_updated",
    #      **product.dict(exclude_unset=True)
    #      # fields : getattr(db_product , fields) for fields in db_product.dict()
    #      }
    #  product_json = json.dumps(product_dict).encode("utf-8")
    #  print("product_json" , product_json)
    #  await producer.send_and_wait("product_topic" , product_json)
    #  session.commit()
    #  session.refresh(db_product)

    #  return db_product



#  todo.content = todo_update.content
#     todo.description = todo_update.description
#     todo.is_done = todo_update.is_done
#     session.add(todo)

# @app.delete("/product/{product_id}" , response_model= Product)
# async def delete_product(product_id : int ,
#                          producer : Annotated[AIOKafkaProducer, Depends(AIOKafkaConsumer)],
#                          session : Annotated[Session , Depends(get_db)]
#                          ):
#      db_product = session.get(Product, product_id)
#      if not db_product:
#         raise HTTPException(status_code=404, details = "Product Not Found")

#      await producer.send_and_wait("my_topic", str(db_product).encode("utf-8"))
#      session.delete(db_product)
#      session.commit()
#      return db_product
 
 
@app.delete("/product/{product_id}", response_model= Product)	
async def delete_product(product_id : int , session : Annotated[Session, Depends(get_db)],
                    producer : Annotated[AIOKafkaProducer, Depends(kafka_producer)]
                   ):
    db_product = session.get(Product, product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail = "Product Not Found")
    product_dict = {field : getattr(db_product, field) for field in db_product.dict()}
    product_json = json.dumps(product_dict).encode("utf-8")
    print("product_json" , product_json)
    session.delete(db_product)
    session.commit()
    try:
        event = {"event_type" : "Product_Deleted" , "product" : product_dict}
        await producer.send_and_wait(setting.KAFKA_PRODUCT_TOPIC , json.dumps(event).encode("utf-8"))
        print("Deleted_Product Send to Kafka topic")
    except Exception as e:
        print("Error sending to Kafka:", e)
    return db_product