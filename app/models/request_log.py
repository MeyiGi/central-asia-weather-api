from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class RequestLog(Base):
    """Logs every API request in order to track usage patterns"""

    __tablename__ = "request_logs"

    id = Column(Integer, primary_key=True, index=True)
    endpoint = Column(String, nullable=False)         
    requested_time = Column(String, nullable=False)
    status = Column(String, nullable=False) 
    error_message = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
