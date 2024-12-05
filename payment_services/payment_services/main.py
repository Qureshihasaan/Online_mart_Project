from aiokafka import AIOKafkaProducer
from fastapi import Depends, FastAPI 
from contextlib import asynccontextmanager
from typing import Annotated, AsyncGenerator
from sqlmodel import Session, select
from .producer import kafka_producer
from .database import create_db_and_tables, get_db 
import asyncio
from .model import Payment , payment_response
import json
from fastapi import HTTPException
from .consumer import consume_messages
from . import setting



@asynccontextmanager
async def lifespan(app : FastAPI)->AsyncGenerator[None,None]:
    print("Tables Creating...")
    task = asyncio.create_task(consume_messages(setting.KAFKA_PAYMENT_TOPIC, setting.BOOTSTRAP_SERVER))
    create_db_and_tables()
    yield


app : FastAPI = FastAPI(lifespan=lifespan , version="1.0.0")




@app.post("/create_payment/" , response_model=payment_response)
async def create_payment(payment : Payment, session : Annotated[Session, Depends(get_db)],
                         producer : Annotated[AIOKafkaProducer, Depends(kafka_producer)]
                         ):
    # payment = Payment(user_id=user_id, order_id=order_id, amount=amount , status="Pending")
    payment_dict = {field : getattr (payment, field) for field in payment.dict()}
    payment_json = json.dumps(payment_dict).encode("utf-8")
    print("Payment_json" , payment_json)
    session.add(payment)
    session.commit()
    session.refresh(payment)
    try:
        event = {"event_type" : "Payment_Created" , "payment" : payment.dict()}
        await producer.send_and_wait(setting.KAFKA_PAYMENT_TOPIC, json.dumps(event).encode('utf-8'))
        print("Payment Details Send to kafka topic....")
    except Exception as e:
        print(f"Error Sending to Kafka {e}")
        session.rollback()
        raise HTTPException(status_code=500, detail="Error Sending payment to kafka..")
    return payment
    # payment.status = "Completed"
    # session.add(payment)
    # session.commit()
    

    # return {"payment_id": payment.id, "status":payment.status}

    

@app.get("/get_all_payment")
async def get_all_payment(session : Annotated[Session, Depends(get_db)]):
    payment = session.exec(select(Payment)).all()
    return payment


@app.get("/get_single_payment")
async def get_single_payment(payment_id : int , session : Annotated[Session, Depends(get_db)]):
    payment = session.get(Payment, payment_id)
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment


@app.put("/update_payment")
async def update_payment(payment_id : int, Payment : Payment, session : Annotated[Session, Depends(get_db)]):
    db_payment = session.get(Payment, payment_id)
    if not db_payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    payment_data = Payment.dict(exclude_unset=True)
    for key, value in payment_data.items():
        setattr(db_payment, key, value)
    payment_dict = {field : getattr (db_payment, field) for field in db_payment.dict()}
    payment_json = json.dumps(payment_dict).encode("utf-8")
    session.add(db_payment)
    session.commit()
    session.refresh(db_payment)
    return db_payment


@app.delete("/delete_payment")
async def delete_payment(payment_id : int, session : Annotated[Session, Depends(get_db)]):
    payment = session.get(Payment, payment_id)
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    session.delete(payment)
    session.commit()
    return {"Message" : "Payment Deleted"}