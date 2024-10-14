
from aiokafka import AIOKafkaProducer

        
async def kafka_producer1():
    producer = AIOKafkaProducer(bootstrap_servers=str("broker:19092"))
    await producer.start()
    try: 
        yield producer
    finally : 
        await producer.stop()
