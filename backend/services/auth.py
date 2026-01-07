from datetime import datetime, timedelta, timezone
from typing import Optional, Any
from jose import jwt
from passlib.context import CryptContext
from backend.core.config import Settings

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    """
    Service for authentication tasks including password hashing and JWT handling.
    Follows 'Dependency Quarantine' by wrapping passlib and python-jose.
    """
    
    def __init__(self, settings: Settings):
        self.settings = settings
        self.algorithm = settings.ALGORITHM
        self.secret_key = settings.SECRET_KEY.get_secret_value()

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verifies a plain password against its hash."""
        return pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str) -> str:
        """Generates a bcrypt hash of the password."""
        return pwd_context.hash(password)

    def create_access_token(self, data: dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
        """Creates a signed JWT access token."""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=self.settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

    def decode_token(self, token: str) -> Optional[dict[str, Any]]:
        """Decodes and validates a JWT token."""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except Exception:
            # Fail Secure: return None on any decoding failure
            return None
