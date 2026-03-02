from datetime import datetime
from sqlalchemy.orm import Session

from app.models.request_log import RequestLog


class RequestLogRepository:
    """DB operations for RequestLOG"""

    def __init__(self, db: Session):
        self._db = db

    def create(
        self,
        endpoint: str,
        requested_time: datetime,
        status: str,
        error_message: str | None = None,
    ) -> RequestLog:
        log = RequestLog(
            endpoint=endpoint,
            requested_time=requested_time,
            status=status,
            error_message=error_message,
        )
        self._db.add(log)
        self._db.commit()
        self._db.refresh(log)
        return log

    def get_all(self, limit: int = 100) -> list[RequestLog]:
        return (
            self._db.query(RequestLog)
            .order_by(RequestLog.created_at.desc())
            .limit(limit)
            .all()
        )
