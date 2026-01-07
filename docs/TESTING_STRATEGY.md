# 🧪 Backend Testing Strategy

This document serves as the **Single Source of Truth** for all testing activities in VibeFinance. We follow a "Defense in Depth" approach to testing, ensuring that financial data is handled with extreme precision and security.

## 1. The "Testing Triad"

Our pipeline enforces three layers of verification:

1.  **Strict TDD (Unit Tests):** Tests must be written *before* implementation. We use `pytest` for execution.
2.  **Mutation Testing:** We use `mutmut` to ensure our tests actually catch bugs. We aim for a **100% Mutation Kill Rate** on critical financial logic.
3.  **Property-Based Testing:** We use `Hypothesis` to fuzz-test mathematical functions (e.g., currency conversion, tax calculation) against millions of generated inputs.

## 2. Unit Test Case Rules

All unit tests must adhere to the following rules:

### 2.1. Data-Driven Testing
**Goal:** Avoid "Magic Numbers" and "Happy Path" bias.
*   **Rule:** Never hardcode a single test value if the logic handles a range.
*   **Tool:** Use `pytest.mark.parametrize` to inject multiple inputs.
*   **Example:**
    ```python
    @pytest.mark.parametrize("amount, expected", [
        (Decimal("100.00"), Decimal("10.00")),
        (Decimal("0.00"), Decimal("0.00")),
        (Decimal("-50.00"), ValueError),
    ])
    def test_calculate_tax(amount, expected):
        ...
    ```

### 2.2. Factories over Fixtures
**Goal:** Decouple tests from database schema changes.
*   **Rule:** Do not manually instantiate models (e.g., `User(id=1, name="John")`).
*   **Tool:** Use `polyfactory` factories (e.g., `UserFactory.build()`).
*   **Why:** If the `User` model adds a required field, you update the Factory once, not 500 tests.

### 2.3. Mocking Boundaries
**Goal:** Test *your* code, not the library's.
*   **Rule:** Mock all external I/O (Database, API calls, Filesystem).
*   **Exception:** For integration tests, use a real (Dockerized) test database, never mocks.

### 2.4. Explicit Assertions
**Goal:** Clarity on failure.
*   **Rule:** Use simple `assert` statements with descriptive error messages if the condition is complex.

## 3. Directory Structure

```
backend/tests/
├── conftest.py          # Global Fixtures (Settings, DB Session)
├── factories.py         # Polyfactory Model Factories
├── test_auth_service.py # Unit tests for Auth Service
└── models/              # Unit tests for Database Models
    └── test_user.py
```

## 4. Execution Commands

*   **Run All Tests:** `pytest`
*   **Run Mutation Tests:** `mutmut run --paths-to-mutate=backend/services`
*   **Run Property Tests:** `pytest -m hypothesis`
