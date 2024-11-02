# from asyncio import tasks
# from typing import Annotated
# from aiokafka import AIOKafkaProducer
# import json
# from fastapi import Depends
# import asyncio
# from product_services.product_services.database import Product
# from .main import kafka_producer


# async def send_product_event(producer : Annotated[AIOKafkaProducer , Depends(kafka_producer)],
#                              event:dict
#                              ):
#     await producer.start()
#     try : 
#         event_data = json.dumps(event).encode('utf-8')
#         await producer.send_and_wait("product-topic", event_data)
#     finally:
#         await producer.stop()


# async def publish_product_event(producer , event_type , product):
#     event={
#         "event_type" : event_type,
#         "product_id" : product["id"],
#         "product_name" : product["name"],
#         "product_price" : product["price"],
#         "product_quantity" : product["quantity"]
#     }

#     await producer.send(event)


# async def handle_product_event(producer , event_type, product):
#     if event_type == "product_created":
#         await publish_product_event(producer, event_type, product)
#     elif event_type == "product_updated":
#         await publish_product_event(producer, event_type, product)
#     elif event_type == "product_deleted":
#         await publish_product_event(producer, event_type, product)


# async def publish_event_for_many_products(producer, event_type, products):
#     tasks = []
#     for product in products:
#         tasks.append(handle_product_event(producer, event_type, product))
#     await asyncio.gather(*tasks)

from aiokafka import AIOKafkaProducer
import json



async def publish_event(producer: AIOKafkaProducer , event: dict):
    event_data = json.dumps(event).encode('utf-8')
    await producer.send_and_wait("product-topic", event_data)