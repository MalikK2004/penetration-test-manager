from sqlalchemy import Column, Integer, String, JSON, DateTime
from datetime import datetime
from . import Base

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    endpoint = Column(String, index=True)
    request_payload = Column(JSON)
    response_payload = Column(JSON)
    status_code = Column(Integer)
    ip_address = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
