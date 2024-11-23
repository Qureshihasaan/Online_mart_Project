from starlette.config import Config
from starlette.datastructures import Secret

try: 
    config = Config(".env")

except FileNotFoundError:
    config = Config("")


DATA_BASE_URL = config("DATA_BASE_URL" , cast=Secret)

TEST_DATABASE_URL = config("TEST_DATABASE_URL", cast=Secret)

KAFKA_USER_TOPIC = config("KAFKA_USER_TOPIC", cast=str)


KAFKA_ORDER_CREATED_TOPIC = config("KAFKA_ORDER_TOPIC", cast=str)


KAFKA_TOPIC_FOR_ORDER_CANCELLED = config("KAFKA_TOPIC_FOR_ORDER_CANCELLED", cast=str)   

KAFKA_TOPIC_FOR_PAYMENT_DONE = config("KAFKA_TOPIC_FOR_PAYMENT_DONE", cast=str)


KAFKA_CONSUMER_GROUP_ID_FOR_NOTIFICATION_SERVICE = config("KAFKA_CONSUMER_GROUP_ID_FOR_NOTIFICATION_SERVICE", cast=str)


KAFKA_BOOTSTRAP_SERVER = config("KAFKA_BOOTSTRAP_SERVER", cast=str)

SENDER_EMAIL = config("SENDER_EMAIL", cast=str)
SENDER_PASSWORD = config("SENDER_EMAIL_PASSWORD", cast=str)   