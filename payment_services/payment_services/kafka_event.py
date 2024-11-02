# from .main import payment
# from .producer import kafka_producer
# import json


# def publish_payment_event(payment):
#     producer = kafka_producer(
#         bootstrap_servers=str("broker:19092"),
#         value_serializer=lambda v: json.dumps(v).encode("utf-8"),
#     )

#     payment_event = {
#         "payment_id": payment.id,
#         "order_id": payment.order_id,
#         "amount": payment.amount,
#         "status": payment.status,
#     }