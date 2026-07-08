# Software Requirements Specification (SRS) - NetConnect

This document describes the functional, non-functional, and user requirements for the NetConnect application.

---

## 1. Project Scope & Definitions

### Scope
NetConnect is a self-contained local web application consisting of a FastAPI backend and a Streamlit frontend. It is designed to act as an offline-first assistant (with template fallback) and online LLM-augmented generator for professional conversational templates.

### Definitions
- **Conversation Starter (Icebreaker)**: A short, 1-3 sentence customized introductory question or statement.
- **Theme**: An extracted key phrase/domain representing a core topic discussed at an event (e.g. "Smart Grid").
- **Few-Shot Learning**: A machine learning prompting technique where the model is supplied with positive historical examples to align its output format and tone.

---

## 2. User Stories

| ID | As a... | I want to be able to... | So that I can... |
| :--- | :--- | :--- | :--- |
| **US-01** | Event Attendee | Enter event details and my personal interests | Receive custom conversation starters relevant to both. |
| **US-02** | Confident Peer | Look up technical terms quickly | Understand technical topics in real-time. |
| **US-03** | Returning User | View history logs of past generations | Recall what templates were created. |
| **US-04** | Active Networker | Click thumbs-up or down on generated templates | Refine the generator's tone to match my style. |
| **US-05** | Privacy-Minded User | Enter my own Gemini API Key in the interface | Ensure my private API keys are not saved on external servers. |

---

## 3. Functional Requirements

### FR-01: User Input Form
- The system must capture an `event_description` (string, 3-500 characters) and `interests` (string, 3-500 characters).
- The system must provide a sidebar to override the default Google Gemini API Key.

### FR-02: Theme Extraction
- The system must extract up to 3 core themes from the provided event description and user interests.
- In offline mode, the system must parse and clean terms using a regex/keyword fallback matching system.

### FR-03: Conversation Starter Generation
- The system must generate exactly 3 distinct conversation starters per request.
- If a Gemini API Key is available, generation must use few-shot prompt injection.
- If offline or keyless, the system must generate icebreakers using pre-configured contextual templates.

### FR-04: Fact Verification (Search)
- The system must allow users to search for topics.
- The system must query Wikipedia APIs to pull a brief description summary (extract) and desktop page URL.

### FR-05: History Logging
- The system must persist each generated session in a database (SQLITE).
- Each history record must track: Event description, interests, serialised themes, generated starters, feedback rating, and creation timestamp.

### FR-06: Feedback System
- The system must allow users to toggle feedback (likes/dislikes) for each history item.
- The database record must update immediately upon clicking.

---

## 4. Non-Functional Requirements

### NFR-01: Performance & Latency
- Offline fallback generation must complete in under 500 milliseconds.
- Online Gemini API generation must complete in under 3 seconds under normal network operations.

### NFR-02: Security & Privacy
- Custom user-provided Gemini API Keys must be processed in memory and never stored in the database.
- Database credentials and API keys must be loaded via environment variables (.env).

### NFR-03: Portability & Installability
- The project must run cross-platform (Windows, macOS, Linux).
- Project installation must be simplified using a single `requirements.txt` file and run via a single orchestrator (`run.py`).

### NFR-04: Reliability
- If the Gemini API endpoint fails (e.g. rate limits, network loss), the system must gracefully catch the error and execute fallback template generation, returning a warning to the user rather than throwing a system crash (HTTP 500).
