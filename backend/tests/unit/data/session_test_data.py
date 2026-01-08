from datetime import datetime, timedelta

# Test Cases Structure: (token_type, is_active, expiration_offset_hours, should_pass, expected_error)

SESSION_VERIFICATION_CASES = [
    # (id, is_active, expiry_delta_hours, expect_success, error_fragment)
    ("valid_active", True, 1, True, None),
    ("revoked_inactive", False, 1, False, "revoked"),
    ("expired_active", True, -1, False, "expired"),
]
