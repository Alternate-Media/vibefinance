from datetime import datetime, timedelta, timezone
from typing import Optional, Any
from jose import jwt
from passlib.context import CryptContext
from sqlmodel import Session
from backend.core.config import Settings
from backend.models.session import UserSession

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

    def create_access_token(
        self,
        data: dict[str, Any],
        db: Optional[Session] = None,
        expires_delta: Optional[timedelta] = None,
    ) -> str:
        """
        Creates a signed JWT access token and persists a session if DB is provided.
        """
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(
                minutes=self.settings.ACCESS_TOKEN_EXPIRE_MINUTES
            )

        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)

        if db:
            # Create UserSession
            # We store the signature or hash of the token to key the session
            # For simplicity in this iteration, we use the token signature logic or just hash the whole token.
            # Plan said "token_hash".
            # To invoke "Single Active Device" logic (or Tracked Sessions), we just add it now.
            try:
                user_id = int(data.get("sub"))
            except (ValueError, TypeError):
                # Should not happen if data is correct
                return encoded_jwt

            user_session = UserSession(
                token_hash=self.get_password_hash(
                    encoded_jwt
                ),  # Using bcrypt for token storage is slow but secure. Or we can use SHA256.
                # Actually, standard practice is SHA256 for token lookup.
                # But for now, let's just use the encoded string if length permits?
                # UserSession.token_hash is max 64. JWT is much longer.
                # So we MUST hash it.
                # Using sha256 via passlib or hashlib?
                # Let's use hashlib for speed as it's just an indentifier.
                # Wait, UserSession.token_hash is PK.
                user_id=user_id,
                device_info="Unknown",  # TODO: device info from request
                expires_at=expire,
                created_at=datetime.utcnow(),
            )

            # Note: real implementation needs hashlib.
            import hashlib

            token_digest = hashlib.sha256(encoded_jwt.encode()).hexdigest()
            user_session.token_hash = token_digest

            db.add(user_session)
            db.commit()  # Or flush if managed transaction

        return encoded_jwt

    def decode_token(self, token: str) -> Optional[dict[str, Any]]:
        """Decodes and validates a JWT token."""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except Exception:
            # Fail Secure: return None on any decoding failure
            return None

    def verify_session(self, token: str, db: Session) -> Any:
        """
        Verifies that the token corresponds to an active, non-expired session in the DB.
        """
        # 1. Decode generic checks (exp, signature)
        payload = self.decode_token(token)
        if not payload:
            raise Exception("Invalid Token")

        # 2. Re-create token hash for lookup
        import hashlib
        token_digest = hashlib.sha256(token.encode()).hexdigest()
        
        # 3. Lookup in DB using SQLModel select
        from sqlmodel import select
        statement = select(UserSession).where(UserSession.token_hash == token_digest)
        session_record = db.exec(statement).first()
        
        if not session_record:
            raise Exception("Session Invalid or Unknown")

        if not session_record.is_active:
            raise Exception("Session Revoked")
            
        if session_record.expires_at < datetime.utcnow():
            raise Exception("Session Expired")
            
        return session_record
