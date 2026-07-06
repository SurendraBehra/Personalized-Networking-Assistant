# Personalized Networking Assistant
An AI-powered web application designed to help professionals and socializers generate smart, context-aware, and highly personalized conversation starters for networking events. It also provides quick, keyless fact verification from Wikipedia and keeps a database of past generations to improve future suggestions based on thumbs up/down user feedback.

## Key Features
1. **Personalized Conversation Starter Generator**
   - **Context-Aware:** Inputs event descriptions and personal interests to extract key themes.
   - **AI-Powered (Gemini):** Integrates with Google Generative AI (using Gemini 1.5 Flash) to write professional, engaging, open-ended starter questions.
   - **Few-Shot Feedback Loop:** Automatically retrieves past starters that received a "thumbs-up" rating and feeds them to the LLM to learn and improve future recommendations.
   - **Robust Fallback:** If no API key is provided, a dynamic, template-based NLP engine constructs context-relevant starters so the app remains fully functional immediately.

2. **Quick Fact Verification**
   - **Search & Summarize:** Search for topics, tech trends, or buzzwords (e.g., *blockchain in healthcare*, *zero knowledge proofs*) directly from Wikipedia.
   - **Concise Summaries:** Fetches compact summaries via the Wikipedia REST API, making it easy to brush up on a topic seconds before a conversation.
   - **Direct References:** Provides a direct, high-quality URL link to the official desktop article for deeper reading.

3. **History & Feedback Dashboard**
   - **Persistent Storage:** Saves all generated sessions (event details, interests, themes, starters) in a local SQLite database.
   - **Feedback Mechanism:** Allows users to rate generated lists (Helpful/Unhelpful).
   - **Train the Model:** High-rated entries are automatically loaded as historical examples in future AI generations.


## Technology Stack
- **Backend:**
  - Python 3.10+ (Tested on 3.13)
  - FastAPI (REST APIs with automated CORS and schema definitions)
  - SQLAlchemy (SQL database toolkit & ORM)
  - SQLite (Local, serverless database)
  - Google GenAI SDK (`google-generativeai` for Gemini model access)
  - Wikipedia API (Public MediaWiki and REST API integrations)
- **Frontend:**
  - Streamlit (Fast, clean, responsive UI dashboard)
  - Custom HTML/CSS (Embedded styles overriding generic layouts for premium aesthetics)
- **Convenience Utilities:**
  - `python-dotenv` (Environment variable management)
  - `run.py` (Multi-process launcher script to run frontend + backend together)


## Project Directory Structure
Personalized Networking Assistant/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py            # FastAPI Entrypoint
│   │   ├── config.py          # Environment configuration
│   │   ├── database.py        # SQLAlchemy Setup & DB session
│   │   ├── models.py          # Database models (SQLite)
│   │   ├── schemas.py         # Pydantic schemas (requests/responses)
│   │   ├── routers/
│   │   │   ├── starters.py    # Starter generator endpoints
│   │   │   ├── facts.py       # Fact check endpoints
│   │   │   └── history.py     # History and feedback endpoints
│   │   └── services/
│   │       ├── theme_extractor.py  # AI/NLP theme extraction
│   │       ├── text_generator.py   # AI/Template starter generator
│   │       ├── fact_verifier.py    # Wikipedia API integration
│   │       └── db_service.py       # DB CRUD transactions
│   ├── tests/
│   │   ├── test_services.py   # Unit tests for services (mocked)
│   │   └── test_routers.py    # Routing & DB integration tests
│   └── requirements.txt
├── frontend/
│   ├── app.py                 # Streamlit UI layout
│   ├── style.css              # Custom CSS stylesheet
│   └── requirements.txt
├── .env                       # Local environment configurations (ignored)
├── .env.example               # Env template
├── requirements.txt           # Unified dependency lists
├── run.py                     # Convenience launch script
└── README.md


## Configuration (.env)

Duplicate `.env.example` to create a `.env` file in the project root:

```bash
# FastAPI Configuration
HOST=127.0.0.1
PORT=8000
DATABASE_URL=sqlite:///./networking_assistant.db

# LLM API Configuration (Optional: template mode is used if not provided)
# Get a key from Google AI Studio: https://aistudio.google.com/
GEMINI_API_KEY=your_gemini_api_key_here
```

*Note: You can also update the Gemini API Key directly inside the Streamlit web application sidebar!*


## How to Run the App

You can run the entire system (both backend and frontend) with a single command!

### 1. Install Dependencies
Run from the root directory:
```bash
pip install -r requirements.txt
```

### 2. Run the Application
Start both the backend server and frontend Streamlit server concurrently:
```bash
python run.py
```

### 3. Open in Browser
- **Streamlit Frontend:** [http://127.0.0.1:8501](http://127.0.0.1:8501)
- **FastAPI Documentation (Swagger):** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)


## Running Unit & Integration Tests

We have written robust tests utilizing `unittest` (Python Standard Library) and `fastapi.testclient.TestClient` with an in-memory SQLite database setup.

To execute tests, run:
```bash
python -m unittest discover -s backend/tests
```

## Example Behavior

### Input:
- **Event Description:** `AI for Sustainable Cities. Discussion on urban carbon reduction and smart infrastructure.`
- **Your Interests:** `climate change, smart infrastructure, machine learning models`

### Extracted Themes (Badges):
- `AI for Sustainable Cities`
- `Smart Infrastructure`
- `Climate Change`

### Output Conversation Starters:
1. *"Hi! I was thinking about the event topic, and it got me wondering: how do you see the intersection of AI for Sustainable Cities and Climate Change evolving in the next couple of years?"*
2. *"It's fascinating how AI for Sustainable Cities is impacting the industry. What do you think is the biggest bottleneck professionals face when integrating it with Smart Infrastructure?"*
3. *"I'm really interested in both AI for Sustainable Cities and Smart Infrastructure. Are you currently working on any projects that bring these two areas together?"*

## Error Handling
- **Empty Fields:** Promptly warns users if mandatory fields are missing.
- **Offline / Wikipedia Failures:** Catches networking exceptions and provides friendly descriptions rather than crashing the client.
- **Missing API Keys:** Swaps seamlessly to dynamic offline templates and alerts users of the configuration state.
