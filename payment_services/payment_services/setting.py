from starlette.config import Config
from starlette.datastructures import  Secret


try:
    config = Config(".env")
except FileNotFoundError:
    config = Config("")


DATA_BASE_URL = config("DATA_BASE_URL" , cast=Secret)

TEST_DATABASE_URL = config("TEST_DATA_BASE_URL" , cast=Secret)

KAFKA_CONSUMER_GROUP_ID_FOR_PAYMENT = config("KAFKA_CONSUMER_GROUP_ID_FOR_PAYMENT" , cast=str)

KAFKA_PAYMENT_TOPIC = config("KAFKA_PAYMENT_TOPIC" , cast=str)

BOOTSTRAP_SERVER = config("BOOTSTRAP_SERVER" , cast=str)