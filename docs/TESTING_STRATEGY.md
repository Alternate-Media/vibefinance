# 🧪 Backend Testing Strategy

This document serves as the **Single Source of Truth** for all testing activities in VibeFinance. We follow a "Defense in Depth" approach to testing, ensuring that financial data is handled with extreme precision and security.

Our testing strategy is divided into three distinct levels of verification.

## 🏆 Level 1: Unit Tests (The Testing Triad)

This layer focuses on logic verification, mathematical correctness, and security boundaries within the code.

### 1.1 The Triad
1.  **Strict TDD:** Tests must be written *before* implementation. We use `pytest` for execution.
2.  **Mutation Testing:** We use `mutmut` to ensure our tests actually catch bugs. We aim for a **100% Mutation Kill Rate** on critical financial logic.
3.  **Property-Based Testing:** We use `Hypothesis` to fuzz-test mathematical functions (e.g., currency conversion, tax calculation) against millions of generated inputs.

### 1.2 Unit Test Rules
*   **Data-Driven Testing:** Use `pytest.mark.parametrize` to inject multiple inputs. Never hardcode single values for range logic.
*   **Factories over Fixtures:** Use `polyfactory` factories (e.g., `UserFactory.build()`) to decouple tests from DB schema changes.
*   **Mocking Boundaries:** Mock all external I/O (Database, API calls, Filesystem).

---

## 🔗 Level 2: Integration Tests (API Testing)

This layer validates the interaction between the application and its dependencies (PostgreSQL, Reverse Proxy) in a controlled CI environment.

### 2.1 Execution Strategy
*   **Environment:** Tests run in a CI pipeline with real, dockerized dependencies (Postgres, Nginx).
*   **Tooling:** A specialized **Testing Agent Application** (HTTP Client) acts as the test driver, simulating API requests.
*   **Batching:**
    *   **Standard CI Run:** A small, randomized batch of API tests is invoked on every commit to ensure rapid feedback.
    *   **Full Suite:** An option exists to trigger the full integration suite (e.g., nightly or before merge).

### 2.2 Scope
*   Verifies end-to-end API workflows (e.g., "Create User -> Login -> Add Transaction").
*   Validates database constraints, transaction rollbacks, and error handling.
*   Ensures the API contract (BFF) remains consistent.

---

## 🖥️ Level 3: Regression, UI & Performance Tests

The final layer ensures the user experience is flawless and performance meets standards.

### 3.1 Regression Testing
*   **Mandate:** **100% Automation** for all regression scenarios.
*   **Coverage:** **100% Coverage** of critical user paths.
*   **Goal:** Prevent re-occurrence of resolved bugs.

### 3.2 UI & Performance Testing
*   **Tool:** **Playwright** (Browser-based testing).
*   **UI Testing:** Validates the Vue.js frontend, user interactions, and visual integrity across resolutions.
*   **Performance:**
    *   Measures load times, rendering performance, and API latency under simulated user load.
    *   Ensures the "Vibe" (fluidity/responsiveness) remains intact.

---

## 📂 Directory Structure

```
backend/tests/
├── unit/                # Level 1: Unit Tests
│   ├── conftest.py
│   ├── factories.py
│   └── ...
├── integration/         # Level 2: API/Integration Tests
│   └── ...
└── ui/                  # Level 3: Playwright Tests
    └── ...
```

## ⚡ Execution Commands

All tests are executed via the project **Makefile**.

*   **Level 1 (Unit):** `make test-unit`
*   **Level 1 (Mutation):** `make test-mutation`
*   **Level 1 (Property):** `make test-hypothesis`
*   **Level 2 (Integration):** `make test-integration`
*   **Level 3 (UI):** `npx playwright test` (Integration pending in Makefile)