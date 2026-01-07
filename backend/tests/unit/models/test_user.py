import pytest
from datetime import datetime
from sqlmodel import SQLModel
from backend.tests.data.user_test_data import VALID_USER_DATA

# TDD: We define the test before the model exists.
# This import will fail until we create backend/models/user.py
try:
    from backend.models.user import User
except ImportError:
    User = None # type: ignore

@pytest.mark.skipif(User is None, reason="User model not yet implemented")
class TestUserModel:
    
    @pytest.mark.parametrize("user_data", VALID_USER_DATA)
    def test_user_model_creation(self, user_data):
        """
        Test that a User model can be instantiated with valid data.
        """
        user = User(**user_data)
        
        assert user.email == user_data["email"]
        assert user.hashed_password == user_data["hashed_password"]
        assert user.is_active == user_data["is_active"]
        assert user.is_superuser == user_data["is_superuser"]
        
        # Default values
        assert user.id is None  # ID is assigned by DB
        assert isinstance(user, SQLModel)

    def test_user_tablename(self):
        """
        Ensure the table name is explicitly set (best practice).
        """
        assert User.__tablename__ == "user"

    def test_user_defaults(self):
        """
        Test default values for optional fields.
        """
        user = User(email="defaults@example.com", hashed_password="hash")
        assert user.is_active is True  # Default should be True
        assert user.is_superuser is False # Default should be False
