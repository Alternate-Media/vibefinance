# Test Cases: backend/tests/unit

**Total Test Cases:** 3

## 📄 `backend/tests/unit/test_auth_service.py`

| Category | Test Case | Expectation | Line |
|----------|-----------|-------------|------|
| **AuthService** | Password Integrity | Plaintext passwords are never stored; verification works only with correct plaintext. | [Go](test_auth_service.py#L5) |
| **AuthService** | Token Cycle | Access tokens are generated as strings and contain all payload data and expiration. | [Go](test_auth_service.py#L23) |
| **AuthService** | Invalid Tokens | Malformed or invalid tokens return None (Fail Secure). | [Go](test_auth_service.py#L43) |

