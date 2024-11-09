from . import setting
from aiokafka import AIOKafkaProducer

        
async def kafka_producer1():
    producer = AIOKafkaProducer(
        bootstrap_servers=setting.BOOTSTRAP_SERVER
    )
    await producer.start()
    try: 
        yield producer
    finally : 
        await producer.stop()
