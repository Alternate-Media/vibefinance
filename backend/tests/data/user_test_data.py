# Test data for User Model tests

VALID_USER_DATA = [
    {
        "email": "test@example.com",
        "full_name": "Test User",
        "hashed_password": "hashed_secret_password",
        "is_active": True,
        "is_superuser": False,
    },
    {
        "email": "admin@vibefinance.in",
        "full_name": "Admin User",
        "hashed_password": "hashed_admin_password",
        "is_active": True,
        "is_superuser": True,
    },
]

INVALID_EMAILS = [
    "not-an-email",
    "missing-at-sign.com",
    "@missing-username.com",
]
