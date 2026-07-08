# Brainstorming Session Notes: NetConnect

## 1. Feature Brainstorming & Prioritization

During the initial brainstorming, we mapped out several potential features and classified them using the MoSCoW framework:

### Must-Have
- Input form for Event Description and User Interests/Expertise.
- Dynamic extraction of event themes.
- Generation of at least 3 conversation starters.
- Local historical logging of generated starters.
- Interactive thumbs-up/thumbs-down ratings (Feedback loop).

### Should-Have
- Quick wiki search tool (Fact Checker) to look up unfamiliar terminology.
- Few-shot learning integration, feeding highly rated (liked) historical starters back into the generation prompt.
- Session-specific Gemini API Key override in UI.

### Could-Have
- Social media/LinkedIn profile URL parser (to auto-extract interests).
- Multi-model selection dropdown (Gemini vs OpenAI vs Claude).
- Starred/favorites folder for quick template caching.

### Won't-Have (For MVP)
- Multi-user authentication and cloud accounts.
- Speech-to-text input dictation.

---

## 2. Technical Stack Brainstorming

### Frontend Options
- *React / Next.js*: High flexibility, but requires significant setup time and API glue-code.
- *Streamlit*: Highly reactive, fast Python-only rendering, handles state and layout cleanly. Perfect for ML/AI dashboards.
- **Decision**: **Streamlit** was chosen for rapid prototyping and clean UI aesthetics.

### Backend Options
- *Flask*: Lightweight but lacks native asynchronous execution, automatic request/response body parsing, and interactive documentation.
- *FastAPI*: Built on Starlette and Pydantic. Supports async out-of-the-box, type safety, and automatic OpenAPI/Swagger docs generation.
- **Decision**: **FastAPI** was chosen for a production-grade, highly performant, type-safe API.

### Database Options
- *PostgreSQL*: Production-grade, but introduces local installation overhead for developers.
- *SQLite*: Serverless, lightweight, store as a local file, fully supported by SQLAlchemy.
- **Decision**: **SQLite** for development and local distribution, with SQLAlchemy abstraction to allow switching to PostgreSQL in production.

### AI Engine Options
- *Local Models (e.g., Llama via Ollama)*: Offline capability, but high hardware requirements.
- *Google Gemini API (`gemini-1.5-flash`)*: High context window, extremely fast, cost-effective, and excellent zero/few-shot performance.
- **Decision**: **Google Gemini API** with a custom local rule-based template **fallback** for offline operations.
