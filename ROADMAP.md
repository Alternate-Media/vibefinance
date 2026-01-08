# 🗺️ VibeFinance Roadmap

This document outlines the planned features, infrastructure enhancements, and security milestones for VibeFinance.

## 🚀 Phase 1: MVP (Q1 2026)
- [x] Basic Project Skeleton (FastAPI + Vue 3).
- [x] Hardened Dockerization (Ubuntu 24.04).
- [x] Application-Level Encryption (ALE) Service.
- [ ] User Authentication & Single-Session Management.
- [ ] Core Assets Tracking (Banking, Liabilities, Equity).
- [ ] Dashboard Overview (Net Worth & Allocation).

## 🛡️ Phase 2: Security & Infra Hardening
- [ ] **Infrastructure Exploration:** Evaluate migration to [Docker Hardened Images (DHI)](https://www.docker.com/products/hardened-images/) for further attack surface reduction.
- [ ] Hardware Security Key support (WebAuthn/FIDO2).
- [ ] Automated Security Audits in CI.
- [ ] Blind Indexing for encrypted field searches.

## 🇮🇳 Phase 3: Indian Ecosystem Integration
- [ ] Automated import for Indian Banks (via SMS parsing or Account Aggregator APIs).
- [ ] Real-time NSE/BSE stock price integration.
- [ ] Mutual Fund (CAS) statement import.
- [ ] Tax Loss Harvesting insights (LTCG/STCG calculation).

## 🎨 Phase 4: UX & Visualization
- [ ] Mobile-Responsive PWA (Progressive Web App).
- [ ] Interactive Asset Allocation charts.
- [ ] Dark Mode / Custom Themes.
- [ ] Multi-currency support (with INR as default).

## 🤖 Active Agent Tasks
- [x] Evaluate Project State ([Report](./docs/planning/evaluation_report.md)) <!-- AGENT -->
- [ ] Documentation & Decision Analysis ([Plan](./docs/planning/implementation_plan.md)) <!-- AGENT -->
- [ ] Initialize Frontend (Vue 3 + Vite) <!-- AGENT -->
- [ ] Fix Backend User Model (Optimistic Locking) <!-- AGENT -->
