from starlette.config import Config
from starlette.datastructures import Secret

try : 
    config = Config(".env")

except FileNotFoundError:
    config = Config("")


DATA_BASE_URL =config("DATA_BASE_URL" , cast=Secret)

BOOT_STRAP_SERVER =config("BOOT_STRAP_SERVER" , cast=str)

KAFKA_ORDER_TOPIC =config("KAFKA_ORDER_TOPIC" , cast=str)

KAFKA_CONSUMER_GROUP_ID_FOR_ORDER=config("KAFAK_CONSUMER_GROUP_ID_FOR_ORDER" , cast=str)

TEST_DATABASE_URL =config("TEST_DATABASE_URL" , cast=Secret)

KAFKA_TOPIC_FROM_USER_TO_ORDER = config("KAFKA_TOPIC_FROM_USER_TO_ORDER", cast=str)


# SECRET_KEY = config("SECRET_KEY" , cast=str)
# ALGORITHM = config("ALGORITHM", cast=str)

# KAFKA_PAYMENT_TOPIC =config("PAYMENT_REQUEST_TOPIC", cast=str)