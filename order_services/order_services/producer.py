from aiokafka import AIOKafkaProducer



async def kafka_producer():
    producer = AIOKafkaProducer(bootstrap_servers = str("broker:19092"))
    await producer.start()
    try: 
        yield producer
    finally:
        await producer.stop()
