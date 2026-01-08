import uuid
from datetime import datetime, timezone

from decimal import Decimal
from typing import Optional, Dict, Any
from enum import Enum
from pydantic import field_validator
from sqlmodel import SQLModel, Field, Column, JSON, Numeric

class AssetType(str, Enum):
    SAVINGS = "SAVINGS"
    FD = "FD"
    RD = "RD"
    PPF = "PPF" # Public Provident Fund
    SCSS = "SCSS" # Senior Citizen Savings Scheme
    FLEXI_RD = "FLEXI_RD"
    EQUITY = "EQUITY"
    MUTUAL_FUND = "MUTUAL_FUND"

class Asset(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    # Ownership
    user_id: int = Field(foreign_key="user.id", index=True, description="Owner")
    
    # Core Identity
    name: str = Field(index=True, description="User-friendly nickname like 'Main Savings'")
    institution_name: str = Field(index=True, description="Bank, Exchange, or Wallet Name")
    
    # Classification
    type: AssetType = Field(index=True)
    
    # Financial Details
    currency: str = Field(default="INR")
    purpose: Optional[str] = Field(default=None, description="Goal: Retirement, Education")
    
    # First-Class Columns (Specifics)
    # Using Decimal for rates. 7.5% -> 7.50. Scale 5, Precision 2 (Max 999.99)
    interest_rate: Optional[Decimal] = Field(default=None, sa_column=Column(Numeric(5, 2)))
    
    # Status
    is_active: bool = Field(default=True)
    
    # Flexible leftovers (Account Numbers, ISIN, Folio Number)
    # Using JSON column for flexibility
    details: Dict[str, Any] = Field(default={}, sa_column=Column(JSON))

    @field_validator("type", mode="before")
    @classmethod
    def validate_type(cls, v: Any) -> Any:
        # Explicit validation because sometimes SQLModel/Pydantic can be lenient with str Enums on init
        if isinstance(v, str):
            try:
                # This ensures it's a valid enum value
                return AssetType(v)
            except ValueError:
                raise ValueError(f"'{v}' is not a valid AssetType")
        return v

    @field_validator("name", "institution_name")
    @classmethod
    def validate_non_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Field cannot be empty")
        return v

