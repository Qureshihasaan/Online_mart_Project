from aiokafka import AIOKafkaProducer
from . import setting
import json

async def kafka_producer():
    producer = AIOKafkaProducer(bootstrap_servers=setting.BOOTSTRAP_SERVER,
                        # value_serializer=lambda v: json.dumps(v).encode('utf-8'),                            
                                )
    await producer.start()
    try:
       yield producer
    finally:
        await producer.stop()



# def publish(topic: str, event : dict):
#     producer = AIOKafkaProducer(bootstrap_servers=setting.BOOTSTRAP_SERVER,
#                         value_serializer=lambda v: json.dumps(v).encode('utf-8'),
#                                 )
#     try:
#         producer.send_and_wait(topic, event)
#         producer.flush()
#     finally:
#         producer.stop()  
