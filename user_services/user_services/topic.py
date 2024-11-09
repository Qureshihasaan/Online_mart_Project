from aiokafka.admin import AIOKafkaAdminClient , NewTopic
from . import setting




async def create_topic():
    admin_client = AIOKafkaAdminClient(
        bootstrap_servers=setting.BOOTSTRAP_SERVER,
    )
    await admin_client.start()
    topic_list = [
        NewTopic(
            name=setting.KAFKA_USER_TOPIC,
            num_partitions=1,
            replication_factor=1,
        ),
        NewTopic(
            name=setting.KAFKA_TOPIC_FROM_USER_TO_ORDER,
            num_partitions=1,
            replication_factor=1,
        )
    ]
    # topic_list.append(setting.KAFKA_USER_TOPIC , )
    # topic_list.append(setting.KAFKA_TOPIC_FROM_USER_TO_ORDER)

    try:
        await admin_client.create_topics(new_topics=topic_list, validate_only=False)
        print("Topics Creating....")
    
    except Exception as e:
        print(f"Error creating topics: {e}")
    
    finally:
        await admin_client.close()
    
  


