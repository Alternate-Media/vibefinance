# 💎 GEMINI.md - Agentic Context & Project Knowledge

> **This file serves as the "Long-Term Memory" and "High-Level Context" for AI Agents (Gemini/Copilot) working on VibeFinance.**
> **It summarizes critical architectural decisions, strict constraints, and the "why" behind them.**

## ⚖️ Priority Hierarchy
1. **Application Security** (Highest)
2. **Maintainability** (Low Debt / Community-Friendly)
3. **User Experience (UX)**
4. **Test Coverage**
5. **Documentation**
6. **Features**
7. **Performance** (Lowest)

## 📜 Development Commandments

1.  **Explicit over Implicit:** No "magic" code or dynamic metaprogramming. No generic `*args/**kwargs`. Every argument and return type must be explicitly typed.
2.  **Fail Secure:** Default to "Deny." Any failure in auth, permission, or decryption must result in a safe state (403 or empty response), never a leak or fallback.
3.  **Dependency Quarantine:** Wrap all 3rd-party libraries in a service/wrapper layer. Business logic should never import external libraries directly.
4.  **Data Minimization:** Sanitized logging only. Never log PII, financial balances, or encryption keys. Use `<REDACTED>` placeholders.
5.  **No Global State:** Use Dependency Injection (FastAPI `Depends`) for database sessions, configurations, and user context. Global variables are forbidden.

6.  **Localization-First:** Default to Indian Numbering System (Lakhs/Crores) for UI. Store time in UTC, display in User Local (Default IST). Use i18n keys for all text.
7.  **Append-Only Financial State:** Historical financial data is immutable. Never overwrite a balance; create a new time-stamped record. Deletions must be "Soft Deletes" (`is_active=False` or `deleted_at=timestamp`) to preserve the audit trail.
8.  **Structured Commits:** Follow [Conventional Commits](https://www.conventionalcommits.org/) (e.g., `feat:`, `fix:`, `chore:`, `refactor:`) to maintain a clean, navigable git history.

## 🧱 Architectural Pillars (Non-Negotiable)

### 1. Data Integrity & Precision
*   **The "No Float" Policy:**
    *   `float` is **FORBIDDEN** for any monetary calculation or storage.
    *   Use `Decimal` (Python) and `NUMERIC(20, 2)` (Postgres) exclusively.
    *   Inputs/Outputs via API must be strings or strict decimal types, never JSON numbers.
*   **Concurrency:**
    *   **Optimistic Locking** is enforced. All DB models must have a `version_id`.
    *   Updates must check `version_id` to prevent lost updates.

### 2. Security Strategy
*   **Single Active Device:**
    *   A user can be logged in multiple places, but only **one** device is "Active" at a time. New activity invalidates or locks other sessions.
*   **Application-Level Encryption (ALE):**
    *   **Data at Rest:** Sensitive columns (PII, Account Numbers, Balances) are encrypted **before** they hit the database.
    *   **Aggregation:** SQL aggregations (`SUM`, `AVG`) are impossible on encrypted data. We fetch raw data, decrypt in memory, and aggregate in Python.

### 3. Testing Standards ("The Triad")
*   **Strict TDD:** Tests are written *before* implementation.
*   **Mutation Testing:** We use `mutmut`. 100% Code Coverage is not enough; we need 100% "Mutant Kill Rate" on critical paths.
*   **Property-Based Testing:** We use `Hypothesis` for all financial math to fuzz-test edge cases.
*   👉 **[Detailed Testing Strategy](./docs/TESTING_STRATEGY.md)**

### 4. API & Frontend
*   **Pattern:** **BFF (Backend-for-Frontend)**.
    *   The backend exposes "Summary" endpoints (e.g., `/dashboard/overview`) that pre-aggregate data.
    *   Avoid "Chatty" APIs where the frontend makes 20 calls.
*   **Philosophy:** **Smart Backend, Dumb Frontend**.
    *   Vue.js handles UX and Visuals.
    *   No complex business logic or math in JavaScript.

## 📂 Code Structure Rules

### Micro-Files
*   **Rule:** One Class = One File.
*   **Goal:** Keep context windows small and precise.
*   **Example:** `models/user.py`, `models/wallet.py` (NOT `models.py`).

### Context-First
*   **Rule:** Every major directory **MUST** have a `.context.md` file explaining its purpose, dependencies, and "Do's and Don'ts".

## 🧠 Decision Log
For a detailed analysis of architectural trade-offs (e.g., Security vs. Search, CI Latency), refer to:
👉 **[DECISIONS.md](./DECISIONS.md)**

## 🛠️ Stack Specifics
*   **Backend:** Python 3.12+, FastAPI, SQLModel (SQLAlchemy + Pydantic).
*   **Frontend:** Vue 3, Vite, TypeScript.
*   **DB:** PostgreSQL 16+.
*   **Infra:** Docker Compose (Single Node).

---
*Updated: 2026-01-08*
