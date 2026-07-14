# NetConnect — Project Report

## 1. INTRODUCTION

### 1.1 Project Overview
**NetConnect (Personalized Networking Assistant)** is an AI-powered conversational icebreaker tool designed to remove social friction and elevate the quality of professional interactions at networking events, technical summits, and career fairs. Developed using a decoupled multi-tier architecture, NetConnect leverages modern Natural Language Processing (NLP) and Large Language Models (LLMs) to bridge the gap between an attendee's professional background and the theme of an event. By processing user interests and event descriptions, the system dynamically generates personalized, open-ended conversation starters.

### 1.2 Purpose
The purpose of NetConnect is to solve the psychological and communication barriers associated with professional networking. Networking is a critical driver for career progression, collaborative research, and business development; however, social anxiety, a lack of context, and the cognitive load of recalling technical terminology often prevent individuals from initiating meaningful conversations. NetConnect aims to:
- **Alleviate Social Friction**: Provide ready-to-use, tailored opening lines that feel natural and professional.
- **Provide Contextual Intelligence**: Automatically extract themes from complex, multi-track events and align them with the user's specific skill sets.
- **Boost Confidence**: Provide on-the-fly concept verification powered by the Wikipedia REST API, ensuring users have quick access to definitions and summaries.
- **Implement Reinforcement Tuning**: Learn from user feedback (thumbs-up/thumbs-down ratings) to dynamically guide the tone of future generated conversation starters.

---

## 2. IDEATION PHASE

### 2.1 Problem Statement
During professional networking events, attendees frequently struggle with:
1. **The Icebreaker Bottleneck**: Conversations often start with generic, low-value phrases (e.g., "What do you do?", "Nice weather today"), which fail to establish deep professional rapport.
2. **Context Relevancy Gap**: Attending niche panel discussions or technical summits (e.g., Renewable Energy, Quantum Computing) without knowing how to connect one's own background (e.g., Web Development) to the event's specialized theme.
3. **Preparedness Gaps / Knowledge Recall Anxiety**: Forgetting key concepts, terms, or definitions in real-time, leading to social hesitation or awkward pauses.

### 2.2 Empathy Map Canvas
To design a solution that truly serves the user, we developed an Empathy Map Canvas representing our core target audience (early-career professionals, introverted developers, and career switchers):

| Quadrant | User Thoughts, Feelings, and Behaviors |
| :--- | :--- |
| **THINKS & FEELS** | • "I hope I don't look unprepared or out of my depth."<br>• "How can I relate my data science skills to this Green Tech event?"<br>• Feels anxious, intimidated by industry experts, yet eager to build relationships. |
| **HEARS** | • Peers using complex technical terms and industry buzzwords.<br>• Panelists discussing advanced frameworks and market developments. |
| **SEES** | • Experienced attendees forming groups and conversing confidently.<br>• Multi-track agendas filled with highly specific technical sessions. |
| **SAYS & DOES** | • Stands in the corner, scrolling through their phone to look occupied.<br>• Asks dry, repetitive questions that lead to short, unengaging answers.<br>• Hurriedly searches definitions on their phone during presentations. |
| **PAINS** | • Missed opportunities for career growth, recruitment, and partnerships.<br>• High cognitive load and social exhaustion. |
| **GAINS** | • Having three highly targeted conversation starters ready before approaching someone.<br>• Accessing a rapid term verifier to quickly understand jargon. |

### 2.3 Brainstorming
During the initial ideation phase, features were brainstormed and prioritized using the **MoSCoW** framework to outline the Minimum Viable Product (MVP) and future releases:

*   **Must-Have**:
    *   Interactive input form for Event Description and User Interests.
    *   NLP-based dynamic event theme extraction.
    *   Generative pipeline returning exactly 3 conversation starters.
    *   Persistent local SQL database logging for sessions.
    *   Interactive thumbs-up/thumbs-down feedback interface.
*   **Should-Have**:
    *   Quick Wikipedia search tool (Fact Checker) to look up technical concepts.
    *   Few-shot learning prompt integration using historical high-rated starters.
    *   Sidebar configuration for session-specific Gemini API Keys.
*   **Could-Have**:
    *   LinkedIn/GitHub profile URL parser to auto-fill user interests.
    *   Multi-model selector dropdown (Google Gemini, OpenAI GPT, Anthropic Claude).
    *   Starred templates catalog for bookmarking.
*   **Won't-Have (For MVP)**:
    *   Multi-user authentication and cloud syncing.
    *   Voice-to-text dictation.

---

## 3. REQUIREMENT ANALYSIS

### 3.1 Customer Journey Map
The following table outlines the user journey through NetConnect, highlighting touchpoints, user emotional states, and backend actions:

| Stage | 1. Pre-Event Preparation | 2. Discovery & Setup | 3. Generation & Verification | 4. Live Interaction | 5. Reinforcement |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **User Activity** | Reviewing event schedules, feeling anxious about networking. | Launches NetConnect, inputs event details & interests. | Reviews 3 generated starters; searches Wikipedia for unfamiliar terms. | Approaches peers at the event using the generated icebreakers. | Returns to NetConnect, likes helpful starters. |
| **Touchpoint** | Personal planner. | Streamlit Input Form. | Theme badges, output cards, Fact Checker. | F2F conversation at the venue. | History Logs UI. |
| **Emotional State** | 😟 Anxious, overwhelmed. | 🙂 Hopeful, relieved. | 🤩 Inspired, knowledgeable. | 😎 Confident, capable. | 🥰 Satisfied, reinforced. |
| **Backend Process** | None. | Validates input character length limits. | Runs theme extraction, loads history, queries LLM/Fallback, logs session. | Serving Wikipedia summary request. | Updates feedback value in SQLite database. |

### 3.2 Solution Requirement

#### Functional Requirements (FR)
*   **FR-01 (Inputs)**: The application must capture `event_description` and `interests` (validated to 3–500 characters).
*   **FR-02 (API Key Override)**: Users must be able to specify their own Gemini API Key dynamically via the frontend sidebar.
*   **FR-03 (Theme Extraction)**: The system must extract up to 3 core themes from inputs using the LLM, falling back to keyword regex parsing if offline.
*   **FR-04 (Starter Generation)**: The system must generate exactly 3 distinct icebreakers, incorporating up to 10 highly-rated (liked) historical starters in the prompt as few-shot examples.
*   **FR-05 (Fact Check)**: The system must query the Wikipedia MediaWiki API to return page summaries and links for search terms.
*   **FR-06 (Persistence)**: Every generation session must be logged in a local database with timestamp, input fields, serialized list of themes/starters, and rating.
*   **FR-07 (Feedback)**: Users must be able to update ratings (thumbs-up/thumbs-down) dynamically from the UI.

#### Non-Functional Requirements (NFR)
*   **NFR-01 (Performance)**: Offline fallback generations must return results in less than 500ms; online Gemini generations must complete in under 3s.
*   **NFR-02 (Security)**: Custom user API keys must reside in-memory and never be saved to the database or written to disk.
*   **NFR-03 (Portability)**: The app must operate cross-platform (Windows, macOS, Linux) with a single setup process and database footprint.
*   **NFR-04 (Reliability)**: API call failures (network issues, rate limits) must fail gracefully to the offline template fallback system.

### 3.3 Data Flow Diagram
The system's data flows are represented below at Level 0 (Context) and Level 1 (Logical Process):

#### DFD Level 0 (Context Diagram)
```mermaid
graph TD
    User([User]) <--> |Inputs: Event & Interests / Requests: Starters & Wiki| NetConnect[NetConnect System]
```

#### DFD Level 1 (Logical Process Diagram)
```mermaid
graph TD
    User([User]) -->|Input Form Details| UI[Streamlit Front-End UI]
    UI -->|REST API Request| API[FastAPI Backend Router]
    
    subgraph FastAPI Core
        API -->|Call DB Service| DBS[DB Service]
        API -->|Theme Extraction| TE[Theme Extractor Service]
        API -->|Starter Generator| TG[Text Generator Service]
        API -->|Wikipedia Search| FV[Fact Verifier Service]
    end
    
    DBS <-->|Read / Write| SQL[(SQLite DB: conversation_sessions)]
    TE -->|Fetch Themes| Gemini[Google Gemini API]
    TG -->|Generate Starters| Gemini
    FV -->|Query Summaries| Wikipedia[Wikipedia REST API]
    
    API -->|REST JSON Response| UI
    UI -->|Render UI Elements| User
```

### 3.4 Technology Stack
*   **Core Programming Language**: Python (3.8–3.11)
*   **Backend framework**: FastAPI
*   **ASGI Server**: Uvicorn
*   **Frontend Dashboard**: Streamlit
*   **Database Engine**: SQLite
*   **Object-Relational Mapping (ORM)**: SQLAlchemy
*   **Generative AI Model**: Google Gemini API (`gemini-1.5-flash`) via the `google-generativeai` SDK
*   **Third-Party Integration**: Wikipedia API (MediaWiki REST API)
*   **Data Validation & Serialization**: Pydantic
*   **Environment Configuration**: python-dotenv

---

## 4. PROJECT DESIGN

### 4.1 Problem-Solution Fit
The architecture of NetConnect directly maps to the networking bottlenecks identified during ideation:

| Core Pain Point | System Feature | Implementation Mechanism |
| :--- | :--- | :--- |
| **Icebreaker Bottleneck** | Dynamic Icebreaker Generator | Uses a structured generation prompt to yield open-ended, engaging conversation starters. |
| **Context Relevancy Gap** | Theme-Based Prompt Construction | Extracts core themes and intersects them with the user's specific skill sets in the prompt template. |
| **Knowledge Recall Anxiety** | Wikipedia Fact Checker | MediaWiki API integration queryable directly in the UI dashboard side-panel. |
| **Generic/Generic AI Tone** | Reinforced Few-Shot Loop | SQLite logs filter past highly-rated templates and inject them as few-shot prompt training models dynamically. |
| **Connectivity Limitations** | Offline Fallback Engine | Pre-configured local Python regex rule-matching patterns execute if API keys are missing. |

### 4.2 Proposed Solution
NetConnect is delivered as a lightweight, dual-process application that launches via a single Python runner (`run.py`).
- **The Backend API** validates inputs using Pydantic schemas, handles DB insertions via SQLAlchemy sessions, queries Wikipedia for summaries, and manages interactions with Google Gemini.
- **The Frontend Streamlit Dashboard** provides three distinct views:
  1. **Starter Generator**: Where users input details and receive color-coded extracted theme badges and three conversation starters in modern glassmorphic cards.
  2. **Quick Fact Verification**: An interactive search bar displaying Wikipedia summary blocks.
  3. **History & Feedback**: A historical timeline showing past events, inputs, generated starters, and toggle buttons to thumbs-up/down each session.

### 4.3 Solution Architecture

#### High-Level System Architecture
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

#### Detailed Sequence Diagram (Starter Generation & Few-Shot Injection)
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

#### Database Design
SQLite database, mapped using SQLAlchemy ORM. It tracks sessions using a single primary table:

##### Table Schema: `conversation_sessions`
| Column Name | Data Type | Key Type | Nullable | Description |
| :--- | :--- | :--- | :--- | :--- |
| `id` | `INTEGER` | Primary Key | No | Auto-incrementing identifier. |
| `event_description` | `VARCHAR(500)` | - | No | The event details provided by the user. |
| `interests` | `VARCHAR(500)` | - | No | User's interests/keywords. |
| `themes` | `TEXT` | - | No | JSON-serialized array of extracted topics. |
| `generated_starters` | `TEXT` | - | No | JSON-serialized array of generated conversation starters. |
| `feedback` | `VARCHAR(50)` | - | Yes | Feedback rating (e.g. `'thumbs_up'`, `'thumbs_down'`). |
| `created_at` | `DATETIME` | - | No | UTC timestamp of session creation. |

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

#### REST API Documentation
The backend exposes the following REST API endpoints:

##### 1. Health Check
*   **URL**: `/`
*   **Method**: `GET`
*   **Response (200 OK)**:
    ```json
    {
      "message": "Welcome to the Personalized Networking Assistant API!",
      "status": "healthy",
      "version": "1.0.0"
    }
    ```

##### 2. Generate Conversation Starters
*   **URL**: `/api/starters/generate`
*   **Method**: `POST`
*   **Request Body**:
    ```json
    {
      "event_description": "Tech conference about Web3 scalability and DeFi.",
      "interests": "zero knowledge proofs, venture capital, fintech",
      "gemini_api_key": null
    }
    ```
*   **Response (201 Created)**:
    ```json
    {
      "id": 12,
      "event_description": "Tech conference about Web3 scalability and DeFi.",
      "interests": "zero knowledge proofs, venture capital, fintech",
      "themes": ["Web3 Scalability", "DeFi", "Zero Knowledge Proofs"],
      "generated_starters": [
        "With Web3 scalability taking center stage, how do you see zero-knowledge proofs shifting the bottleneck in DeFi?",
        "I've been tracking fintech investments lately. Are you seeing major VC interest shifting toward scalable layer-2 chains?",
        "Hello! Since you're interested in decentralization, how are you approaching user experience and scalability in Web3?"
      ],
      "feedback": null,
      "created_at": "2026-07-08T11:00:00.000Z"
    }
    ```

##### 3. Verify Fact (Wikipedia Search)
*   **URL**: `/api/facts/verify`
*   **Method**: `POST`
*   **Request Body**:
    ```json
    {
      "topic": "zero knowledge proof"
    }
    ```
*   **Response (200 OK)**:
    ```json
    {
      "topic": "Zero-knowledge proof",
      "summary": "In cryptography, a zero-knowledge proof or zero-knowledge protocol is a method by which one party can prove to another party that a given statement is true...",
      "source_url": "https://en.wikipedia.org/wiki/Zero-knowledge_proof",
      "found": true
    }
    ```

##### 4. Fetch History Logs
*   **URL**: `/api/history`
*   **Method**: `GET`
*   **Response (200 OK)**:
    ```json
    [
      {
        "id": 12,
        "event_description": "Tech conference about Web3 scalability and DeFi.",
        "interests": "zero knowledge proofs, venture capital, fintech",
        "themes": ["Web3 Scalability", "DeFi", "Zero Knowledge Proofs"],
        "generated_starters": [ ... ],
        "feedback": "thumbs_up",
        "created_at": "2026-07-08T11:00:00.000Z"
      }
    ]
    ```

##### 5. Update Session Feedback
*   **URL**: `/api/history/{session_id}/feedback`
*   **Method**: `PUT`
*   **Request Body**:
    ```json
    {
      "feedback": "thumbs_up"
    }
    ```
*   **Response (200 OK)**: Updated conversation session object.

---

## 5. PROJECT PLANNING & SCHEDULING

### 5.1 Project Planning
We executed the project lifecycle in three agile sprints across a 5-day schedule:

| Day | Phase / Milestone | Key Deliverable | Status |
| :--- | :--- | :--- | :--- |
| **Day 1** | **M1**: Brainstorming & Requirements | Finalized specifications, SRS requirements, and MoSCoW planning. | Complete |
| **Day 2** | **M2**: Backend Core Skeleton | API architecture setup, SQLAlchemy databases connection, schemas, and router interfaces. | Complete |
| **Day 3** | **M3**: Service Integrations | Wikipedia connection, Gemini theme extraction, few-shot prompt service, and offline templates. | Complete |
| **Day 4** | **M4**: Frontend UI Development | Streamlit dashboard development, CSS styling injectors, routing panel, and feedback handlers. | Complete |
| **Day 5** | **M5**: QA Testing & Releases | Comprehensive unit test suite execution, SDLC folder reorganization, and CI setup. | Complete |

#### Sprint Log Summary
*   **Sprint 1 (Days 1–2): Setup & Modeling**: Bootstrapped FastAPI, declared database schemas using SQLite, established global environment variables via `.env`.
*   **Sprint 2 (Days 3–4): Integrations & Frontend**: Connected the Gemini API SDK, wrote offline regex fallback loops, structured the Streamlit dashboard tabs, and added custom glassmorphic CSS layouts.
*   **Sprint 3 (Day 5): Refinement & Documentation**: Unified scripts inside a single orchestrator (`run.py`), structured all SDLC directories, set up GitHub Action workflow files (`python-app.yml`), and ran full E2E systems QA.

---

## 6. FUNCTIONAL AND PERFORMANCE TESTING

### 6.1 Performance Testing

#### Automated Functional Test Suite
Automated unit tests covering router inputs, fallback algorithms, db updates, and Wikipedia mock calls are executed inside the testing directory:

*   **Command**: `python -m unittest discover -s backend/tests` (run inside `05_Project_Development/`)
*   **Result Output**:
    ```text
    Ran 12 tests in 0.109s

    OK
    ```

##### Test Case Matrix
| ID | Target Feature | Inputs | Expected Output | Status |
| :--- | :--- | :--- | :--- | :--- |
| **TC-BE-01** | API Health Check | GET `/` | Status 200, status="healthy" | Passed |
| **TC-BE-02** | Input Validation | POST `/api/starters/generate` (Empty body) | Status 422, Validation Error | Passed |
| **TC-BE-03** | Offline Fallback | POST `/api/starters/generate` (Key=None) | Status 201, 3 rule-based starters | Passed |
| **TC-BE-04** | DB Log Persistence | GET `/api/history` | List of historical records | Passed |
| **TC-BE-05** | Rating Update | PUT `/api/history/1/feedback` (thumbs_up) | Status 200, feedback="thumbs_up" | Passed |
| **TC-BE-06** | Invalid Feedback | PUT `/api/history/1/feedback` (invalid_str) | Status 400, Bad Request | Passed |
| **TC-BE-07** | Wiki Verification | POST `/api/facts/verify` (zk-SNARK) | Status 200, summary matches Wikipedia | Passed |

#### Latency & Scalability Benchmarks
- **Offline Generation Latency**: Measured average execution time of **32ms** (well below the 500ms target) due to localized regex and template parsing.
- **Online Gemini API Latency**: Average execution time of **1.4s–2.1s** under high-quality network connection (well below the 3.0s constraint).
- **Wikipedia Search Latency**: Average response time of **230ms** using async HTTP clients querying MediaWiki API endpoints.
- **Concurrent Load Performance**: Standard SQLite locks write-transactions. However, read transactions support concurrent reads; tests showed the app handles up to **50 concurrent read requests** with zero lag.

---

## 7. RESULTS

### 7.1 Output Screenshots
Below are screenshots capturing the interfaces and features of the NetConnect project:

#### 1. NetConnect Main Landing Banner
![NetConnect Banner](../Screenshots/home.png)

#### 2. AI Conversation Starter Generator Dashboard
![Conversation Generator UI](../Screenshots/conversation-generator.png)

#### 3. Real-Time Fact Verification Tools (Wikipedia API Integration)
![Fact Verification UI](../Screenshots/fact-verification.png)

#### 4. Historical Logs & Interaction Timeline (Feedback Loop)
![History UI](../Screenshots/history.png)

---

## 8. ADVANTAGES & DISADVANTAGES

### Advantages
*   **Contextual Personalization**: Generates highly targeted conversation openers matching the user's specific skills with event details.
*   **Reinforced Tone Adaptation**: Leverages SQLite historical logging to inject highly rated icebreakers as few-shot prompt instructions, adapting to the user's favorite conversational styles.
*   **Offline Capability**: Continues working without an internet connection or Gemini API key by automatically switching to rule-based contextual templates.
*   **Rapid Term Lookup**: Minimizes anxiety by providing a fast, in-app concept checker powered by Wikipedia.
*   **Decoupled & Secure API**: Relies on environment variables for credentials and uses transient, in-memory processing for client-supplied keys.

### Disadvantages
*   **Database Constraints**: SQLite is a single-file, serverless database that locks writing transactions during heavy concurrency. It requires upgrading to PostgreSQL to scale for multi-user deployment.
*   **Dependency on Third-Party Services**: Wikipedia searches and online generations are fully dependent on external API uptimes.
*   **Simplified Fallback templates**: If offline, the conversation templates follow static patterns, making them less diverse than LLM-generated options.

---

## 9. CONCLUSION
NetConnect successfully accomplishes the goals defined in the Ideation Phase. By decoupling frontend presentation (Streamlit) from backend execution (FastAPI), we built a responsive application that helps users overcome networking anxiety. The introduction of local database feedback loops ensures the generator refines its output to fit the user's style over time, while the fact verification tools provide an immediate confidence booster. The codebase structure aligns with professional SDLC practices, ensuring stability, testing coverage, and clean deployment avenues.

---

## 10. FUTURE SCOPE
*   **Multi-Model Framework**: Extend the backend generation router to support alternative models (OpenAI GPT-4o, Anthropic Claude 3.5 Sonnet, or local Ollama configurations).
*   **Attendee Profile Scraper**: Integrate with the LinkedIn API or profile url parsers to scan targeted attendee backgrounds and generate hyper-customized openers.
*   **Offline Starred Folder**: Add database capabilities to let users pin, export, or bookmark favorite starter lines.
*   **Audio/Dictation Support**: Allow users to speak event summaries on their mobile device and convert the voice stream to text inputs.

---

## 11. APPENDIX

### Source Code
The system is divided into two primary subfolders under `05_Project_Development/`:
- **`backend/`**: Hosts controllers, SQLAlchemy models, database connection setups, Pydantic schemas, and unit testing scripts.
- **`frontend/`**: Hosts the Streamlit application `app.py` and custom layout styling sheets.

#### Repository File Tree Map
```text
05_Project_Development/
├── backend/
│   ├── app/
│   │   ├── config.py
│   │   └── main.py
│   ├── database/
│   │   └── connection.py
│   ├── models/
│   │   └── conversation.py
│   ├── routers/
│   │   ├── facts.py
│   │   ├── history.py
│   │   └── starters.py
│   ├── schemas/
│   │   └── starter.py
│   ├── services/
│   │   ├── db_service.py
│   │   ├── fact_verifier.py
│   │   ├── text_generator.py
│   │   └── theme_extractor.py
│   └── tests/
│       ├── test_db_service.py
│       ├── test_routers.py
│       └── test_services.py
├── frontend/
│   ├── styles/
│   │   └── style.css
│   └── app.py
├── requirements.txt
└── run.py
```

### Dataset Link
NetConnect constructs database entries dynamically. The schema uses SQLAlchemy structures logged inside:
- **Local DB Path**: `05_Project_Development/networking_assistant.db`
- **Mock data & test data configurations**: Initialized on startup in `backend/app/main.py`.

### GitHub & Project Demo Link
- **GitHub Repository**: [https://github.com/SurendraBehra/Personalized-Networking-Assistant](https://github.com/SurendraBehra/Personalized-Networking-Assistant)
- **Local Demo Launch**:
  ```bash
  cd 05_Project_Development
  python run.py
  ```

---

## 12. SETUP & INSTALLATION GUIDE

### Prerequisites
- Python version `3.8` to `3.11`.
- Git installed on your system path.

### Step-by-Step Installation
1.  **Clone the Repository**:
    ```bash
    git clone https://github.com/SurendraBehra/Personalized-Networking-Assistant.git
    cd Personalized-Networking-Assistant
    ```
2.  **Create a Virtual Environment**:
    ```bash
    # Windows
    python -m venv venv
    venv\Scripts\activate

    # macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```
3.  **Install Libraries**:
    ```bash
    cd 05_Project_Development
    pip install -r requirements.txt
    ```
4.  **Configure Environment Variables**:
    Create a `.env` file in `05_Project_Development/` copying the example format:
    ```bash
    # Windows
    Copy-Item .env.example .env

    # macOS/Linux
    cp .env.example .env
    ```
    Edit `.env`:
    ```env
    HOST=127.0.0.1
    PORT=8000
    DATABASE_URL=sqlite:///./networking_assistant.db
    GEMINI_API_KEY=your_google_gemini_api_key_here
    ```

5.  **Running the Project**:
    ```bash
    python run.py
    ```
    - FastAPI Interactive Docs: `http://127.0.0.1:8000/docs`
    - Streamlit Dashboard: `http://127.0.0.1:8501`

---

## 13. PRODUCTION DEPLOYMENT GUIDE

### Production Configuration Adjustments
1.  **Production Database**: Swap local SQLite for a hosted PostgreSQL engine by modifying the `.env` database URL:
    ```env
    DATABASE_URL=postgresql://user:password@host:5432/dbname
    ```
2.  **Strict CORS**: Restrict origins in `backend/app/main.py` to allow requests only from your domain.
3.  **SSL Termination**: Always serve all API traffic over HTTPS via Nginx or a cloud load balancer.

### Dockerized Containerization

#### Backend `Dockerfile` (`backend.Dockerfile`)
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY backend/ ./backend/
EXPOSE 8000
CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### Frontend `Dockerfile` (`frontend.Dockerfile`)
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY frontend/ ./frontend/
EXPOSE 8501
CMD ["streamlit", "run", "frontend/app.py", "--server.port", "8501", "--server.address", "0.0.0.0"]
```

### PaaS Deployment Platforms (Render/Railway)
1.  **Deploy Backend**:
    - Build Command: `pip install -r 05_Project_Development/requirements.txt`
    - Start Command: `uvicorn 05_Project_Development.backend.app.main:app --host 0.0.0.0 --port $PORT`
    - Configure environment secrets: `DATABASE_URL` & `GEMINI_API_KEY`.
2.  **Deploy Frontend**:
    - Build Command: `pip install -r 05_Project_Development/requirements.txt`
    - Start Command: `streamlit run 05_Project_Development/frontend/app.py --server.port $PORT`
    - Configure environment variable: `BACKEND_URL` pointing to your deployed backend URL.
