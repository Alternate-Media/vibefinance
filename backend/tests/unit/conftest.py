import pytest
from backend.core.config import Settings
from backend.services.auth import AuthService
from pydantic import SecretStr


@pytest.fixture(scope="session")
def mock_settings():
    """
    Provides a predictable Settings object for testing.
    Using 'session' scope so it's created once per test run.
    """
    return Settings(
        SECRET_KEY=SecretStr("test-secret-key-for-unit-tests-only"),
        ENCRYPTION_KEY=SecretStr("test-encryption-key-must-be-32-chars-long="),
        DATABASE_URL="sqlite:///:memory:",
        ALGORITHM="HS256",
        ACCESS_TOKEN_EXPIRE_MINUTES=30,
        ENVIRONMENT="testing",
    )


@pytest.fixture(scope="session")
def auth_service(mock_settings):
    """
    Provides the AuthService initialized with mock settings.
    """
    return AuthService(mock_settings)

from sqlmodel import create_engine, SQLModel, Session
from sqlalchemy.pool import StaticPool

@pytest.fixture(name="session")
def session_fixture():
    # In-memory SQLite for speed and isolation
    engine = create_engine(
        "sqlite://", 
        connect_args={"check_same_thread": False}, 
        poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
