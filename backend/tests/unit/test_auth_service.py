import pytest
from backend.services.auth import AuthService
from backend.tests.unit.data.auth_test_data import (
    PASSWORD_TEST_CASES,
    TOKEN_PAYLOAD_TEST_CASES,
)


# @TESTCASE: AuthService - Password Integrity
# Expectation: Plaintext passwords are never stored; verification works only with correct plaintext.
@pytest.mark.parametrize("password", PASSWORD_TEST_CASES)
def test_password_hashing_and_verification(auth_service: AuthService, password: str):
    """
    Test that the service correctly hashes and verifies different password types.
    """
    hashed = auth_service.get_password_hash(password)

    # 1. Hash should not match plaintext
    assert hashed != password

    # 2. Verify true for correct password
    assert auth_service.verify_password(password, hashed) is True

    # 3. Verify false for incorrect password
    assert auth_service.verify_password(password + "_wrong", hashed) is False


# @TESTCASE: AuthService - Token Cycle
# Expectation: Access tokens are generated as strings and contain all payload data and expiration.
@pytest.mark.parametrize("payload", TOKEN_PAYLOAD_TEST_CASES)
def test_token_creation_and_decoding(auth_service: AuthService, payload: dict):
    """
    Test that tokens created with various payloads can be decoded correctly.
    """
    token = auth_service.create_access_token(payload)
    assert isinstance(token, str)

    decoded = auth_service.decode_token(token)
    assert decoded is not None

    # Check that all original payload keys exist in decoded token
    for key, value in payload.items():
        assert decoded[key] == value

    # Check that expiration was added
    assert "exp" in decoded


# @TESTCASE: AuthService - Invalid Tokens
# Expectation: Malformed or invalid tokens return None (Fail Secure).
def test_decode_invalid_token(auth_service: AuthService):
    """
    Ensure invalid tokens return None (Fail Secure).
    """
    assert auth_service.decode_token("invalid.token.string") is None
