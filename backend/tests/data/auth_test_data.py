# Test data for Authentication Service tests

PASSWORD_TEST_CASES = [
    "simple",
    "complex!@#123",
    "very_long_" * 10,
    " ",
    "12345678",
    "😊🔑🔐", # Unicode/Emoji
    "パスワード", # Non-Latin script
]

TOKEN_PAYLOAD_TEST_CASES = [
    {"sub": "user_123"},
    {"sub": "user_456", "role": "admin"},
    {"sub": "user_789", "permissions": ["read", "write"]},
    {}, # Empty payload
    {"sub": "user_😊", "data": "🚀"}, # Unicode in values
    {"complex": {"nested": "value"}}, # Nested Dict (JWT claims are JSON)
]
