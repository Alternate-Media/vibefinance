import pytest
from datetime import datetime
from sqlmodel import SQLModel
from backend.tests.unit.factories import UserFactory

# TDD: We define the test before the model exists.
# This import will fail until we create backend/models/user.py
try:
    from backend.models.user import User
except ImportError:
    User = None # type: ignore

@pytest.mark.skipif(User is None, reason="User model not yet implemented")
class TestUserModel:
    
    # @TESTCASE: User Model - Creation
    # Expectation: User objects are correctly instantiated from valid dictionaries.
    def test_user_model_creation(self):
        """
        Test that a User model can be instantiated with valid data using Factory.
        """
        # Generate valid data using the factory
        user_data = UserFactory.build().model_dump(exclude={'id', 'created_at', 'updated_at'})
        
        user = User(**user_data)
        
        assert user.email == user_data["email"]
        assert user.hashed_password == user_data["hashed_password"]
        assert user.is_active == user_data["is_active"]
        assert user.is_superuser == user_data["is_superuser"]
        
        # Default values
        assert user.id is None  # ID is assigned by DB
        assert isinstance(user, SQLModel)

    # @TESTCASE: User Model - Table Name
    # Expectation: The database table name is explicitly set to 'user'.
    def test_user_tablename(self):
        """
        Ensure the table name is explicitly set (best practice).
        """
        assert User.__tablename__ == "user"

    # @TESTCASE: User Model - Default Values
    # Expectation: Optional fields have correct defaults (Active: True, Superuser: False).
    def test_user_defaults(self):
        """
        Test default values for optional fields.
        """
        user = User(email="defaults@example.com", hashed_password="hash")
        assert user.is_active is True  # Default should be True
        assert user.is_superuser is False # Default should be False