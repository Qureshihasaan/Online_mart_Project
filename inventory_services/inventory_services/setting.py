from starlette.config import Config
from starlette.datastructures import Secret

try:
    config = Config(".env")
except FileNotFoundError :
    config = Config("")


DATABASE_URL = config("INVENTORY_DATABASE_URL", cast=Secret)

TEST_DATABASE_URL = config("TEST_DATABASEURL", cast=Secret)

BOOTSTRAP_SERVER = config("BOOTSTRAP_SERVER", cast=str)

KAFKA_TOPIC_FOR_PRODUCT_EVENT = config("KAFKA_TOPIC_FOR_PRODUCT_EVENT", cast=str)

KAFAK_CONSUMER_GROUP_ID_FOR_PRODUCT = config("KAFKA_CONSUMER_GROUP_ID_FOR_INVENTORY", cast=str)