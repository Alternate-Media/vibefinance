---
description: Strict TDD Protocol Implementation
---

# 🛡️ Strict TDD Protocol

This workflow MUST be followed for every feature implementation.

## 1. 🧠 Evaluate & English Test Cases
*   **Goal:** Understand the requirement and define behavior before coding.
*   **Action:** Create/Update a Markdown file (e.g., `docs/specs/feature_name.md`) or use the `task.md` description to list specific test cases in plain English.
*   **Review:** Verify coverage with User (if complex) or self-evaluate against requirements.

## 2. 🔴 Red: Write Unit Test Scripts (Failing)
*   **Goal:** Translate English cases into executable Pytest scripts.
*   **Constraint:** Do NOT write the implementation code yet.
*   **Action:** Create `tests/unit/test_feature.py`. get confirmatgion from user
*   **Verification:** Run the specific test. It MUST fail (Red State).

## 3. 🟢 Green: Write Code via Micro-Steps
*   **Goal:** Write the minimum code to make the test pass.
*   **Action:** Implement logic in `backend/`.
*   **Verification:** Run the specific test. It MUST pass (Green State).

## 4. 🧩 Consolidate & Data-Driven
*   **Goal:** Refactor tests to be robust and cover edge cases.
*   **Action:** Use `pytest.mark.parametrize` to cover standard, edge, and invalid inputs based on the English cases. formalize and store multiple test data for future runs. get confirmation from user
*   **Verification:** Run the specific test file iiwth all data again again.

## 5. 🧪 Run Entire Suite & Generate Results
*   **Goal:** Ensure no regressions.
*   **Action:** Run `make test` (or `make test-unit`).
*   **Output:** Capture the output/results.

## 6. 👤 User Confirmation
*   **Goal:** Get sign-off before committing.
*   **Action:** Use `notify_user` to show the passed test results and code.

## 7. 💾 Git Commit
*   **Goal:** Save the verified state.
*   **Action:** `make git-commit` with a descriptive message (e.g., `feat: implement auth session verification (TDD verified)`).