# Contributing to VibeFinance

Thank you for your interest in contributing! VibeFinance has strict architectural and security standards to ensure financial integrity.

## ⚖️ Priority Hierarchy
1. **Application Security** (Highest)
2. **Maintainability**
3. **User Experience (UX)**
4. **Test Coverage**
5. **Documentation**
6. **Features**
7. **Performance** (Lowest)

## 🛠️ Development Workflow

1. **Strict TDD:** Tests MUST be written before implementation.
2. **Structured Commits:** We follow [Conventional Commits](https://www.conventionalcommits.org/).
   - `feat:` for new features
   - `fix:` for bug fixes
   - `docs:` for documentation changes
   - `refactor:` for code changes that neither fix a bug nor add a feature
3. **Branching:** Use descriptive branch names (e.g., `feat/add-wallet-encryption` or `fix/decimal-rounding`).

## 📜 Coding Commandments

- **Explicit over Implicit:** No "magic" code or dynamic metaprogramming. Strict typing is required everywhere.
- **The "No Float" Policy:** `float` is strictly forbidden for monetary values. Use `Decimal` (Python) and `NUMERIC` (Postgres).
- **Micro-Files:** One Class = One File. Keep context windows small.
- **Dependency Quarantine:** Wrap all 3rd-party libraries in a service/wrapper layer.
- **Fail Secure:** Any failure in auth or decryption must result in a safe, denied state.

## 🧪 Testing Standards
Your PR will not be merged unless it meets:
- 100% Code Coverage.
- 100% Mutation Testing "Kill Rate" on critical paths (using `mutmut`).
- Passing Property-Based tests (using `Hypothesis`) for financial math.

## 🛡️ Security
- Never log PII, financial balances, or encryption keys.
- All sensitive data must be encrypted at the application level (ALE) before hitting the DB.

## 📝 Submitting a PR
1. Fill out the Pull Request template completely.
2. Ensure all linting and type checks pass.
3. Verification from a maintainer regarding security impact is required.
