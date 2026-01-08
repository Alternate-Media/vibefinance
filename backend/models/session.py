from datetime import datetime
from sqlmodel import Field, SQLModel


class UserSession(SQLModel, table=True):
    __tablename__ = "user_session"

    # Token signature (hash) is the PK. We never store the full JWT.
    token_hash: str = Field(primary_key=True, max_length=64)

    user_id: int = Field(foreign_key="user.id", nullable=False, index=True)
    device_info: str = Field(max_length=255)  # e.g. "Chrome on Windows"
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    expires_at: datetime = Field(nullable=False)
    is_active: bool = Field(default=True, nullable=False)

    # We don't strictly need version_id here as sessions are immutable/short-lived,
    # but for consistency with architectural rules we can include it or explicitely omit.
    # Given they are read-heavy and delete-only (logout), we omit for now.
