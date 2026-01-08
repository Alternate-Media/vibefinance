# 🏗️ Core Features Implementation Plan

## Goal Description
Address critical "Phase 1 MVP" gaps identified during project evaluation. This includes initializing the Frontend, enforcing Security (Single Active Device, Optimistic Locking), and implementing the core Asset/Transaction database schema.

## User Review Required
> [!IMPORTANT]
> **Single Active Device:** Since Redis is not currently in the stack (to keep it "Single Node" simple), I propose implementing session management via a `UserSession` table in PostgreSQL. Login will invalidate previous sessions for that user.

> [!WARNING]
> **Encryption Key:** The current `encryption.py` generates a random key if `ENCRYPTION_KEY` is missing. I will change this to **Fail Secure** (raise error) in production mode, as losing the key means losing data.

## Proposed Changes

### 1. TDD & Factories (Level 1)
#### [NEW] [backend/tests/factories.py](file:///c:/Users/prady/repos/vibefinance/backend/tests/factories.py)
*   Create `UserFactory` using `polyfactory`.
*   Create `UserSessionFactory`, `AssetFactory`, `TransactionFactory`.

### 2. Backend Core (Auth & Security)
#### [NEW] [backend/tests/unit/test_auth_session.py](file:///c:/Users/prady/repos/vibefinance/backend/tests/unit/test_auth_session.py)
*   **Test First:** Implement failing tests for `UserSession` logic.
    *   `@TESTCASE: Auth - Single Active Device Enforecment`
    *   `@TESTCASE: Auth - Token Invalidation on Logout`

#### [MODIFY] [backend/models/user.py](file:///c:/Users/prady/repos/vibefinance/backend/models/user.py)
*   Add `version_id` field (SQLModel Optimistic Locking).

#### [NEW] [backend/models/session.py](file:///c:/Users/prady/repos/vibefinance/backend/models/session.py)
*   Create `UserSession` model.

#### [MODIFY] [backend/services/auth.py](file:///c:/Users/prady/repos/vibefinance/backend/services/auth.py)
*   Update `create_access_token` and `get_current_user` to rely on `UserSession`.

### 3. Backend Assets Schema
#### [NEW] [backend/tests/unit/test_assets.py](file:///c:/Users/prady/repos/vibefinance/backend/tests/unit/test_assets.py)
*   **Test First:** Implement failing tests for Asset creation and Decimal precision.
    *   `@TESTCASE: Assets - Prevent Float Arithmatic`
    *   `@TESTCASE: Assets - Optimistic Locking Update`

#### [NEW] [backend/models/asset.py](file:///c:/Users/prady/repos/vibefinance/backend/models/asset.py)
*   `Asset` model implementation.

#### [NEW] [backend/models/transaction.py](file:///c:/Users/prady/repos/vibefinance/backend/models/transaction.py)
*   `Transaction` model implementation.

### Frontend Initialization
#### [NEW] Frontend Config
*   Execute `npm create vite@latest` logic.
*   Setup `Vue 3`, `TypeScript`, `Bootstrap`.

## Verification Plan

### Automated Tests
*   **Unit Tests:**
    *   Test `User` creation with and without `version_id` updates (verify `StaleDataError`).
    *   Test `AuthService` - Login User A on Device 1, then Login User A on Device 2 -> Device 1 token should fail.
    *   Test `Asset` model - Create asset, verify `0.1 + 0.2` decimal precision.

### Manual Verification
1.  **Backend Health:** Run `make run-backend` and hit `/api/health`.
2.  **Frontend**: Start vite server (`npm run dev`), open browser, see "VibeFinance" welcome page.
3.  **Auth Flow**: Use Swagger UI (`/docs`) to Register -> Login (get token) -> Use token.
