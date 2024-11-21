import logging , asyncio
from aiokafka import AIOKafkaConsumer
from aiokafka.errors import KafkaConnectionError
from . import setting


loop = asyncio.get_event_loop()
logging.basicConfig(level=logging.INFO)

async def consume_messages(topic , bootstrapserver)->AIOKafkaConsumer:
     consumer = AIOKafkaConsumer(
          topic,
          bootstrap_servers=bootstrapserver,
          group_id= setting.KAFKA_CONSUMER_GROUP_ID_FOR_PRODUCT,
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
          