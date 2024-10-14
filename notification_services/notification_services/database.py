from datetime import datetime
from sqlmodel import SQLModel , Field , create_engine
from . import setting
from typing import Optional


class notification_preference(SQLModel , table = True):
    id : Optional[int] = Field(primary_key=True, default=None)
    user_id : int
    email_notification : bool = True
    sms_notification : bool = False

class NotificationLog(SQLModel , table=True):
    id : Optional[int] = Field(primary_key=True , default=None)
    user_id : int
    notification_type : str         ### signup , login , update_order
    sent_at : datetime = Field(default_factory=datetime.utcnow)


connection_strings = str(setting.DATA_BASE_URL).replace(
    "postgresql","postgresql+psycopg2"
)

engine=create_engine(connection_strings , connect_args={} , pool_recycle=300)


def create_db_and_tables()->None:
    SQLModel.metadata.create_all(engine)
