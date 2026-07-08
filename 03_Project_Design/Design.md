# Project Design Specifications - NetConnect

This document details the architectural layout, entity relations, and system workflows for the NetConnect application.

---

## 1. System Architecture

NetConnect uses a decoupled multi-tier architecture dividing UI presentation, API orchestration, and external AI/data services.

```mermaid
graph TD
    User([User]) <--> |Interacts| FE[Streamlit Client]
    FE <--> |JSON REST API| BE[FastAPI Server]
    
    subgraph FastAPI Components
        BE --> Routers[Routers]
        Routers --> Services[Services]
        Services --> DB[(SQLite Database)]
    end
    
    subgraph External APIs
        Services --> |Gemini API Key| LLM[Google Gemini API]
        Services --> |MediaWiki REST API| Wiki[Wikipedia REST API]
    end
```

---

## 2. Dynamic Workflow Design

### A. Conversation Starter Generation Sequence
The generation endpoint (`/api/starters/generate`) routes requests through theme extraction, historical few-shot reinforcement checks, and LLM orchestration.

```mermaid
sequenceDiagram
    autonumber
    actor User
    participant FE as Streamlit UI
    participant BE as FastAPI Router
    participant EXT as ThemeExtractor Service
    participant DB as SQLite DB
    participant GEN as TextGenerator Service
    participant API as Gemini API

    User->>FE: Click "Generate Starters"
    FE->>BE: POST /api/starters/generate
    BE->>EXT: extract_themes(event, interests)
    EXT-->>BE: list of themes
    BE->>DB: query thumbs_up history (Few-Shot data)
    DB-->>BE: list of highly-rated templates
    BE->>GEN: generate_starters(event, interests, themes, few_shot_list)
    GEN->>API: Send structured few-shot prompt
    API-->>GEN: Generated 3 Starters
    GEN-->>BE: list of starters
    BE->>DB: save session record
    DB-->>BE: session ID
    BE-->>FE: Return JSON Response
    FE-->>User: Render starters & feedback buttons
```

### B. Feedback Reinforcement Workflow
User interactions update historical datasets to dynamically direct future generation requests.

```mermaid
graph TD
    A[User reviews starter cards] -->|Clicks thumbs up| B(PUT /api/history/id/feedback)
    B --> C[DB Update: feedback='thumbs_up']
    D[User requests new starters] --> E[System fetches up to 10 feedback='thumbs_up' records]
    E --> F[Inject records as few-shot prompt examples]
    F --> G[Gemini aligns starter tone with liked styles]
```

---

## 3. Database ER Diagram

The local SQLite relational database is mapped using SQLAlchemy ORM to track session records and ratings.

### Table Schema: `conversation_sessions`
- `id` (Integer, Primary Key): Auto-incrementing session index.
- `event_description` (String): Raw event details.
- `interests` (String): Raw user interests.
- `themes` (Text): Serialized JSON array of extracted themes.
- `generated_starters` (Text): Serialized JSON array of generated conversation starters.
- `feedback` (String): Feedback status (NULL, `'thumbs_up'`, or `'thumbs_down'`).
- `created_at` (DateTime): Record creation timestamp (defaults to UTC).

```mermaid
erDiagram
    CONVERSATION_SESSIONS {
        int id PK
        varchar event_description
        varchar interests
        text themes
        text generated_starters
        varchar feedback
        datetime created_at
    }
```
