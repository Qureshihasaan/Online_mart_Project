from fastapi import FastAPI , Depends , HTTPException
from aiokafka import AIOKafkaConsumer , AIOKafkaProducer
from contextlib import asynccontextmanager
import logging
from aiokafka.errors import KafkaConnectionError
import asyncio
from typing import AsyncGenerator , Annotated
from .database import Product , Session , engine , create_db_and_tables
import json
from sqlmodel import select


loop = asyncio.get_event_loop()
logging.basicConfig(level=logging.INFO)

async def consume_messages(topic , bootstrapserver)->AIOKafkaConsumer:
     consumer = AIOKafkaConsumer(
          topic,
          bootstrap_servers=bootstrapserver,
          group_id= "my_group",
          auto_offset_reset= "earliest"
          
     )
     
     # await consumer.start()
     # consumer.subscribe(["my_topic"])
     # return consumer
     
     while True:
          try :
               await consumer.start()
               logging.info("Consumer Started...")
               break
          except KafkaConnectionError as e: 
               logging.info("Consumer staring failed, Retry in 5 sec")
               await asyncio.sleep(5)
                   
                   
     try: 
          async for messages in consumer:
               consume = messages.value
               print("consumer_messages " , consume )
     finally:
          await consumer.stop()
          

     
@asynccontextmanager
async def lifespan(app : FastAPI) -> AsyncGenerator[None , None]:
     print("Tables Creating")
     task = asyncio.create_task(consume_messages( "my_topic" , "broker:19092"))
     create_db_and_tables()
     yield 



app : FastAPI = FastAPI(lifespan=lifespan , version="1.0.0")


def get_db():
    with Session(engine) as session:
        yield session


async def kafka_producer():
     producer = AIOKafkaProducer(bootstrap_servers = str("broker:19092"))
     await producer.start()
     try: 
          yield producer
     finally:
          await producer.stop() 
              
              
              
@app.post("/product" , response_model = Product)
async def product_service(product : Product , producer : Annotated[AIOKafkaProducer , Depends(kafka_producer)],
                          session : Annotated[Session , Depends(get_db)]
                          )->Product:
     product_dict = {field : getattr(product , field) for field in product.dict()}
     product_json = json.dumps(product_dict).encode("utf-8")
     print("Product_json" , product_json)
     await producer.send_and_wait("my_topic" , product_json) #producer
     session.add(product)
     session.commit()
     session.refresh(product) 
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
    
     # for fields , value in product.dict(exclude_unset=True).items():
     #    setattr(db_product , fields, value)
        
     product_dict = {fields : getattr(db_product , fields) for fields in db_product.dict()}
     product_json = json.dumps(product_dict).encode("utf-8")
     print("product_json" , product_json)
     await producer.send_and_wait("my_topic" , product_json)
     session.commit()
     session.refresh(db_product)
     return db_product



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
     product_dict = {fields : getattr(db_product , fields) for fields in db_product.dict()}
     product_json = json.dumps(product_dict).encode("utf-8")
     print("product_json" , product_json)
     producer.send_and_wait("my_topic", db_product)
     session.delete(db_product)
     session.commit()
     return db_product