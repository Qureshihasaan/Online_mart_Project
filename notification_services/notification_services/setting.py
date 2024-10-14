from starlette.config import Config
from starlette.datastructures import Secret

try: 
    config = Config(".env")

except FileNotFoundError:
    config = Config("")


DATA_BASE_URL = config("DATA_BASE_URL" , cast=Secret)

TEST_DATABASE_URL = config("TEST_DATABASE_URL", cast=Secret)

KAFAK_CONSUMER_GROUP_ID_FOR_PRODUCT = config("KAFAK_CONSUMER_GROUP_ID_FOR_PRODUCT" , cast=str)

KAFKA_ORDER_TOPIC = config("KAFKA_ORDER_TOPIC" , cast=str)

BOOT_STRAP_SERVER = config("BOOT_STRAP_SERVER", cast=str)