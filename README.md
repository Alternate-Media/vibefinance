# 💸 VibeFinance

> **A self-hosted, secure financial dashboard vibecoded for the modern Indian investor.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Backend](https://img.shields.io/badge/Backend-FastAPI-009688.svg?style=flat&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Frontend](https://img.shields.io/badge/Frontend-Vue.js-4FC08D.svg?style=flat&logo=vue.js&logoColor=white)](https://vuejs.org/)
[![Database](https://img.shields.io/badge/Database-PostgreSQL-336791.svg?style=flat&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Security](https://img.shields.io/badge/Security-Financial%20Grade-red)](./DECISIONS.md)

**VibeFinance** is a monolithic, highly secure, and rigorously tested personal finance dashboard designed to give you a holistic view of your wealth. Unlike typical budgeting apps that obsess over daily transactions, VibeFinance focuses on the big picture: your **Net Worth** and **Asset Allocation**.

Built with a "Security First" mindset, it is designed to be self-hosted, ensuring your sensitive financial data never leaves your control. The MVP is tailored specifically for the **Indian financial ecosystem**.

---

## 📑 Table of Contents
- [📸 Dashboard Preview](#-dashboard-preview)
- [🎯 Core Mission](#-core-mission)
- [🛡️ Security & Engineering Standards](#-security--engineering-standards)
- [🚀 Features (MVP)](#-features-mvp)
- [🛠️ The Stack](#-the-stack)
- [📜 Development Commandments](#-development-commandments)
- [🏁 Getting Started](#-getting-started)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)

---

## 📸 Dashboard Preview
*(Screenshots coming soon...)*

---

## 🎯 Core Mission

To provide a "vibecoded" (visually immersive, fluid, and responsive), extremely secure, and collaboration-friendly platform for users to track their entire financial holding.

**Key Philosophy:**
*   **Macro over Micro:** We track balances and portfolio values, not the ₹20 you spent on chai.
*   **Security is Paramount:** Self-contained, Dockerized, and designed for private network deployment.
*   **Collaborative Code:** A codebase that is easy to read, strictly typed, and heavily tested to encourage open-source contribution.

---

## 🛡️ Security & Engineering Standards

VibeFinance is built with **uncompromising standards**. We treat personal financial data with the gravity it deserves.

### 🔒 Security Architecture
*   **Financial Grade Security:** Adherence to standard financial data protection guidelines.
*   **Zero-Knowledge Principles:** Application-Level Encryption (ALE) ensures the database only sees ciphertext for sensitive fields.
*   **Local-First:** Data stays on your node. No external analytics or tracking.
*   **Single Active Device:** Strict session management ensures only one device is active at a time.

### ⚙️ Engineering Principles
*   **Data Precision:** Floating-point arithmetic is banned. All money is `Decimal` (2 places).
*   **Testing Triad:** Strict TDD, Property-Based Testing (Hypothesis), and Mutation Testing (mutmut). See [TESTING_STRATEGY.md](./docs/TESTING_STRATEGY.md) for details.
*   **Agentic Development:** The codebase is structured with `.context.md` files and micro-modules to be easily understood by AI agents.

*(See [DECISIONS.md](./DECISIONS.md) for a deep dive into our architectural trade-offs.)*

---

## 🚀 Features (MVP)

Tailored for the Indian market, VibeFinance supports tracking the following asset classes:

*   **🏦 Banking:** Savings & Current Account Balances.
*   **💳 Liabilities:** Credit Card Balances & Loans.
*   **📈 Market Instruments:** Equity (Stocks) & Mutual Funds.
*   **🇮🇳 Indian Savings Schemes:** FD, RD, PPF, EPF.
*   **🛡️ Protection:** Insurance Policies (Term/Health/Life).

---

## 🛠️ The Stack

VibeFinance is a **Monorepo** structured for separation of concerns while maintaining ease of development.

| Layer | Technology |
| :--- | :--- |
| **Frontend** | Vue.js 3 (TypeScript, Composition API) |
| **Backend** | Python 3.12+, FastAPI, SQLModel |
| **Database** | PostgreSQL 16+ |
| **Infra** | Docker Compose (Single Node) |

### Directory Structure
```
vibefinance/
├── backend/        # FastAPI application (SQLModel, API routes)
├── frontend/       # Vue.js SPA application
├── docker/         # Dockerfiles and Nginx config
├── docs/           # Architecture & Security Documentation
├── GEMINI.md       # AI Context & Knowledge Base
└── DECISIONS.md    # Architectural Decision Log
```

---

## 📜 Development Commandments

Contributors must adhere to our 8 core principles:
1.  **Explicit over Implicit:** No "magic" code. Strict typing everywhere.
2.  **Fail Secure:** Default to "Deny." Failures must be safe (no data leaks).
3.  **Dependency Quarantine:** All 3rd-party libs must be wrapped in a service layer.
4.  **Data Minimization:** No PII or financial data in logs.
5.  **No Global State:** Use Dependency Injection.
6.  **Localization-First:** Default to INR (Lakhs/Crores) and IST.
7.  **Append-Only State:** Historical records are immutable. Soft deletes only.
8.  **Structured Commits:** Use Conventional Commits.

---

## 🏁 Getting Started

### Prerequisites
*   **Docker & Docker Compose** (for full stack run)
*   **uv** (for backend python management)
*   **Node.js/npm** (for frontend)

### Quick Start
```bash
git clone https://github.com/Alternate-Media/vibefinance.git
cd vibefinance
make setup         # Installs all dependencies
make docker-up     # Starts DB and Infra
make run-backend   # Starts local backend server
```
Access the dashboard at `http://localhost:80` (via Docker) or `http://localhost:8000` (Local Backend).

## 🧑‍💻 Development
We use a **Makefile** to drive the dev workflow:
*   `make test` - Run unit tests.
*   `make lint` - Run type checks and linters.
*   `make format` - Auto-format code.
*   `make help` - Show all available commands.

---

## 🤝 Contributing

We welcome contributions! Since this project aims to be "extremely tested," please ensure all PRs include relevant tests.

1.  Fork the repo.
2.  Create your feature branch (`git checkout -b feature/amazing-feature`).
3.  Commit your changes (`git commit -m 'feat: Add some amazing feature'`).
4.  Push to the branch (`git push origin feature/amazing-feature`).
5.  Open a Pull Request.

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.


### Agentic Architecture
This project is built using **Agentic Development** principles, ensuring the codebase is an "open book" for both AI agents and human contributors.

*   **Context-First Documentation:** Every major directory contains a `.context.md` file. This file defines the directory's purpose, rules, and boundaries, allowing AI agents to understand the architectural intent without scanning the entire codebase.
*   **Micro-file Principle:** We strictly follow a "One File, One Responsibility" rule. Each database model, API resource, or UI component resides in its own dedicated file. This reduces token overhead for AI tools and minimizes merge conflicts.
*   **Barrel Exports:** To prevent "import hell," each directory uses `__init__.py` (backend) or index files (frontend) to provide clean, unified import paths.
*   **Strict Type Enforcement:** If it isn't typed, it doesn't exist. Python type hints (MyPy/Strict) and TypeScript are mandatory for all contributions.

### API & Frontend Architecture

VibeFinance utilizes a **BFF (Backend-for-Frontend)** architectural pattern to balance security, performance, and ease of debugging.

*   **REST over GraphQL/gRPC:** We prioritize transparency and debuggability. The API uses standard RESTful principles with JSON payloads, making it easy to inspect via browser dev tools or `curl`.
*   **Smart Backend, Dumb Frontend:**
    *   **Backend (The Brain):** Handles all business logic, financial calculations, Application-Level Encryption (ALE), and data aggregation. The backend is the "Source of Truth."
    *   **Frontend (The Vibe):** A lightweight Vue.js SPA focused exclusively on UX, visualizations, and data presentation. It contains minimal business logic to ensure that development remains focused on the backend where the complexity is most manageable and secure.
*   **BFF Summary Endpoints:** Instead of the frontend fetching 20 granular resources, the backend provides aggregate "Summary" endpoints tailored for specific dashboard views. This reduces network chatter and allows the backend to perform batch decryption and analysis in-memory.

## 🏗️ Development & Architecture

The project enforces high standards for code quality:

*   **Testing:** Comprehensive unit and integration tests (pytest/Vitest). **100% Coverage Mandate.**
*   **Type Safety:** Full MyPy strict compliance on backend, TypeScript on frontend.
*   **CI/CD:** Automated pipelines for linting, testing, and security scanning.

### Directory Structure
```
vibefinance/
├── backend/        # FastAPI application (SQLModel, API routes)
├── frontend/       # Vue.js SPA application
├── docker/         # Dockerfiles and Nginx config
├── docs/           # Architecture & Security Documentation
├── docker-compose.yml
└── ...
```

## 🚀 Deployment

VibeFinance is optimized for **Single-Node Deployment** via Docker Compose.
It bundles the Database, Backend, Frontend, and Reverse Proxy into a single, cohesive unit suitable for a VPS, Raspberry Pi, or Home Server.

## 🏁 Getting Started

*(Instructions to be updated as the MVP is built)*

### Prerequisites
*   Docker & Docker Compose

### Quick Start
```bash
git clone https://github.com/Alternate-Media/vibefinance.git
cd vibefinance
docker-compose up --build
```
Access the dashboard at `http://localhost:80` (or your configured port).

## 🤝 Contributing

We welcome contributions! Since this project aims to be "extremely tested," please ensure all PRs include relevant tests.

1.  Fork the repo.
2.  Create your feature branch (`git checkout -b feature/amazing-feature`).
3.  Commit your changes (`git commit -m 'Add some amazing feature'`).
4.  Push to the branch (`git push origin feature/amazing-feature`).
5.  Open a Pull Request.

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.