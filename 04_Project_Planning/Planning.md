# Project Planning & Timeline - NetConnect

This document details the development sprints, milestones, and release schedules for the NetConnect application.

---

## 1. Project Milestones

| Milestone | Title | Key Deliverable | Target Date | Status |
| :--- | :--- | :--- | :--- | :--- |
| **M1** | Project Brainstorming & Requirements | Finalized feature scope, architecture stack, and SRS. | Day 1 | Complete |
| **M2** | Backend Core Skeleton | API setup, SQLAlchemy connection, database migrations, and routers. | Day 2 | Complete |
| **M3** | AI Services Integration | ThemeExtractor, TextGenerator (with Few-Shot logic), and Wikipedia APIs. | Day 3 | Complete |
| **M4** | Frontend Dashboard Development | Streamlit forms, theme badge renders, fact checker, history, and feedback. | Day 4 | Complete |
| **M5** | Reorganization & Release prep | SDLC folder structure migration, CI configuration, and push to GitHub. | Day 5 | Complete |

---

## 2. Sprint Timeline

We executed this project in three focused sprints using an agile Scrum framework:

### Sprint 1: Setup & Data Modeling (Days 1-2)
- **Goal**: Build the API foundation and database integration.
- **Tasks**:
  - Configure FastAPI and Uvicorn.
  - Setup SQLAlchemy and write `conversation_sessions` SQLite model.
  - Design absolute namespace importing.
  - Draft local testing harness.

### Sprint 2: Core Integration & Front-End (Days 3-4)
- **Goal**: Integrate external services and construct the dashboard.
- **Tasks**:
  - Integrate google-generativeai API for theme parsing and starter creation.
  - Build fallback rule-based generation templates for offline support.
  - Create Wikipedia client helper for fact verification searches.
  - Create the Streamlit dashboard layout, adding Custom CSS glassmorphic card stylings.
  - Implement feedback toggle endpoints.

### Sprint 3: Refinement & Releases (Day 5)
- **Goal**: Modularize directories, write documentation, and configure CI/CD pipelines.
- **Tasks**:
  - Reorganize project source files into SDLC portfolio structures under `05_Project_Development/`.
  - Draft comprehensive Markdown documents for architecture, API, setup, and deployment.
  - Setup GitHub Action workflows to run test suites on push/pull requests.
  - Write root-level assets: README.md, LICENSE, CONTRIBUTING.md, CODE_OF_CONDUCT.md, and CHANGELOG.md.
  - Execute full E2E system testing.
