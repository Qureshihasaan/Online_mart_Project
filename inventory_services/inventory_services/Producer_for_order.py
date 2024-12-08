# from aiokafka import AIOKafkaProducer
# from . import setting


# async def producer_for_order_process():
#     producer = AIOKafkaProducer(
#         bootstrap_servers=setting.BOOTSTRAP_SERVER,
#     )
#     while True:
#         try: 
#             await producer.start()
#             yield producer

#         finally:
#             await producer.stop()