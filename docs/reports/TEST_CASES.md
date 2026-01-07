# Global Test Case Report

**Total Test Cases:** 6

## 📄 `backend/tests/unit/models/test_user.py`

| Category | Test Case | Expectation | Line |
|----------|-----------|-------------|------|
| **User Model** | Creation | User objects are correctly instantiated from valid dictionaries. | [Go](test_user.py#L16) |
| **User Model** | Table Name | The database table name is explicitly set to 'user'. | [Go](test_user.py#L36) |
| **User Model** | Default Values | Optional fields have correct defaults (Active: True, Superuser: False). | [Go](test_user.py#L44) |

## 📄 `backend/tests/unit/test_auth_service.py`

| Category | Test Case | Expectation | Line |
|----------|-----------|-------------|------|
| **AuthService** | Password Integrity | Plaintext passwords are never stored; verification works only with correct plaintext. | [Go](test_auth_service.py#L5) |
| **AuthService** | Token Cycle | Access tokens are generated as strings and contain all payload data and expiration. | [Go](test_auth_service.py#L23) |
| **AuthService** | Invalid Tokens | Malformed or invalid tokens return None (Fail Secure). | [Go](test_auth_service.py#L43) |

