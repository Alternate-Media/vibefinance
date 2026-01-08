# 🧠 Architectural Decisions & Trade-offs

This document logs critical architectural decisions, the specific conflicts/pain points they introduce, and the agreed-upon mitigation strategies. It serves as a "Why we did this" reference for future maintainers.

---

## 1. Security vs. Searchability (ALE)

*   **The Constraint:** **Application-Level Encryption (ALE)** is mandatory for "Financial Grade" security. Data is encrypted before reaching the database.
*   **The Conflict:** Standard SQL querying (`WHERE amount > 100`, `LIKE '%keyword%'`) breaks on encrypted strings. Decrypting the entire dataset in-memory to filter it causes massive performance degradation as data grows.
*   **The Decision:** **Balanced Security Strategy.**
    *   **Encrypted Fields (PII/Sensitive):** `Account Numbers`, `Payee/Merchant Names`, `User Notes`, `Detailed Descriptions`.
    *   **Plaintext Fields (Metadata):** `Transaction Amount`, `Transaction Date`, `Category Tags`, `Currency`.
*   **Rationale:** `Amount` and `Date` without context (Who/What) carry low privacy risk but are critical for performant SQL filtering and reporting (e.g., "Show expenses > ₹5000 last month").
*   **Mitigation for Search:** We will use **Blind Indexing** (hashing) for strict equality checks on encrypted fields (e.g., finding all transactions for a specific Account Number) if needed.

## 2. Frontend Latency (Dumb Client)

*   **The Constraint:** **Smart Backend / Dumb Frontend** + **In-Memory Aggregation**.
*   **The Conflict:** The frontend is forbidden from doing complex math. Every currency conversion or "Net Worth" recalculation requires a network round-trip.
*   **The Decision:** **BFF (Backend-for-Frontend) with Caching.**
    *   The backend exposes coarse-grained "Dashboard" endpoints.
    *   **Mitigation:** We will implement short-lived caching (Redis/In-Memory) for expensive aggregation results (e.g., Net Worth) to make the UI feel snappy despite the round-trips.

## 3. Python Import Cycles (Micro-files)

*   **The Constraint:** **Micro-files** (One Class per File).
*   **The Conflict:** SQLModel/SQLAlchemy relies on circular relationships (User -> Wallet -> User). Separating these into files causes Python `ImportError: circular import`.
*   **The Decision:** **Strict Forward Referencing.**
    *   Models must never import other models at the top level for type hinting.
    *   **Mitigation:** Use `typing.TYPE_CHECKING` blocks for IDE hints and String Forward References (e.g., `Relationship(link_model="Wallet")`) for runtime logic.

## 4. CI/CD Speed (Mutation Testing)

*   **The Constraint:** **100% Mutation Kill Rate** target.
*   **The Conflict:** Mutation testing (`mutmut`) is extremely slow (hours for large suites), which blocks rapid development cycles.
*   **The Decision:** **Tiered Testing Pipeline.**
    *   **Local Dev:** Run mutation tests *only* on the specific file being edited (`mutmut run --paths-to-mutate=...`).
    *   **CI (PRs):** Incremental mutation testing on changed files.
    *   **Nightly:** Full suite mutation testing.

## 5. Storage Growth (Append-Only)

*   **The Constraint:** **Append-Only Financial State** (Immutable History).
*   **The Conflict:** High-frequency data (e.g., stock prices updating every minute) will explode the database size if every update is a new row.
*   **The Decision:** **Hybrid Storage Strategy.**
    *   **User Data (Wallets/Txns):** Strictly Append-Only (Audit Trail).
    *   **Market Data (External):** Snapshot/Prune. We keep daily closes history but overwrite real-time intra-day prices.

## 6. Data Consistency (Optimistic Locking)

*   **The Constraint:** **Prevent Lost Updates** in concurrent financial transactions.
*   **The Conflict:** Locking rows (Pessimistic) kills performance and creates deadlocks. Ignoring it leads to data corruption (Last-Write-Wins overwriting balances).
*   **The Decision:** **Optimistic Locking (Enforced via `version_id`).**
    *   Every database model MUST have a `version_id` column.
    *   Updates must include the `version_id` in the `WHERE` clause. If 0 rows are updated, raise `StaleDataError`.
    *   **Mitigation:** Frontend handles retry logic for non-critical stale data errors.

## 7. Numerical Precision (No Floats)

*   **The Constraint:** **Zero Floating-Point Errors.**
*   **The Conflict:** Python's `float` and standard JSON numbers are IEEE 754 (imprecise). `0.1 + 0.2 != 0.3`.
*   **The Decision:** **Exclusive use of `Decimal`.**
    *   Database: `NUMERIC(20, 2)` (or higher precision).
    *   Backend: `decimal.Decimal` only.
    *   API: Money is serialized as `String` (e.g., `"100.50"`) to preserve precision during JSON definition.

## 8. Password Security (Bcrypt Truncation)

*   **The Constraint:** **Bcrypt 72-Byte Limit.**
*   **The Conflict:** Bcrypt silently truncates passwords longer than 72 bytes, meaning `very_long_password_A` and `very_long_password_B` could verify as the same hash effectively weakening security for long passphrases.
*   **The Decision:** **SHA256 Pre-hashing.**
    *   Passwords are effectively hashed twice: `Bcrypt(SHA256(plaintext_password))`.
    *   SHA256 compresses any length input into a fixed 32-byte string (well within Bcrypt's limit).
    *   **Mitigation:** This adds a negligible computation cost for significant correctness and security.
