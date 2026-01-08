import uuid
from datetime import datetime
from decimal import Decimal
from typing import Optional
from sqlmodel import SQLModel, Field, Column, Numeric

class BalanceHistory(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    
    # The Core Data: Value at a specific Time
    timestamp: datetime = Field(default_factory=datetime.utcnow, index=True)
    
    # Link
    asset_id: uuid.UUID = Field(foreign_key="asset.id", index=True)
    
    # Amount with High Precision (20, 2)
    amount: Decimal = Field(default=0, sa_column=Column(Numeric(20, 2)))
    
    # Optional Context
    note: Optional[str] = Field(default=None)
