from .producer import kafka_producer
import json


def publish_payment_event(payment):
    producer = kafka_producer(
    bootstrap_servers=str("broker:19092"),
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    )