import uuid
import enum
from sqlalchemy import Column, String, Integer, Enum, DateTime, ForeignKey, func
from app.database import Base

class TransactionTypeEnum(str, enum.Enum):
    PURCHASE = "purchase"
    RESTOCK = "restock"

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    vehicle_id = Column(String(36), ForeignKey("vehicles.id"), nullable=False)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    type = Column(Enum(TransactionTypeEnum), nullable=False)
    quantity = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
