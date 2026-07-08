# Changelog - NetConnect

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.1.0] - 2026-07-08

### Added
- Professional documentation files: `docs/architecture.md`, `docs/api.md`, `docs/setup.md`, and `docs/deployment.md`.
- Comprehensive Mermaid diagrams for System Architecture, Application Workflow, Database Flow, and API Flow.
- GitHub community files: `LICENSE`, `CONTRIBUTING.md`, `CHANGELOG.md`, and `CODE_OF_CONDUCT.md`.
- GitHub Issue templates (`bug_report.md`, `feature_request.md`) and Pull Request template.
- GitHub Actions workflow (`python-app.yml`) for automated linting and unittest checks on pushes/pull requests.
- Premium screenshot placeholders under `assets/screenshots/`.

### Changed
- Reorganized directory structure by decoupling routers, services, database connection files, models, and schemas from `backend/app/` to professional module packages under `backend/`.
- Updated all import paths across all files to support absolute namespace importing.
- Moved frontend assets and styles into a separate subfolder `frontend/styles/`.

---

## [1.0.0] - 2026-07-06

### Added
- Initial codebase upload containing FastAPI backend and Streamlit frontend.
- SQLite database integration for saving conversation starter histories.
- Google Gemini API integration for theme extraction and conversation starter generation.
- Fallback mode for running locally without Gemini API keys using offline professional templates.
- Wikipedia REST API integration for rapid tech concept verification.
