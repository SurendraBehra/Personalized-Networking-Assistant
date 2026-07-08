# REST API Documentation - NetConnect

The backend server is powered by FastAPI. By default, when the backend is running, you can access the interactive Swagger UI documentation at:
**`http://127.0.0.1:8000/docs`**

---

## 1. Global Endpoints

### Health Check
Returns the current health status and version of the API.

* **URL**: `/`
* **Method**: `GET`
* **Response (200 OK)**:
  ```json
  {
    "message": "Welcome to the Personalized Networking Assistant API!",
    "status": "healthy",
    "version": "1.0.0"
  }
  ```

---

## 2. Conversation Starter Endpoints

### Generate Conversation Starters
Extracts event themes and generates 3 personalized conversation starters.

* **URL**: `/api/starters/generate`
* **Method**: `POST`
* **Request Header**: `Content-Type: application/json`
* **Request Body**:
  | Field | Type | Required | Description |
  | :--- | :--- | :--- | :--- |
  | `event_description` | `string` | Yes | Description of the event (3-500 chars). |
  | `interests` | `string` | Yes | User's professional/personal interests (3-500 chars). |
  | `gemini_api_key` | `string` | No | Custom session-specific Gemini API Key. |

  *Example Payload:*
  ```json
  {
    "event_description": "Tech conference about Web3 scalability and Decentralized Finance.",
    "interests": "zero knowledge proofs, venture capital, fintech",
    "gemini_api_key": null
  }
  ```

* **Response (201 Created)**:
  ```json
  {
    "id": 12,
    "event_description": "Tech conference about Web3 scalability and Decentralized Finance.",
    "interests": "zero knowledge proofs, venture capital, fintech",
    "themes": [
      "Web3 Scalability",
      "Decentralized Finance",
      "Zero Knowledge Proofs"
    ],
    "generated_starters": [
      "With Web3 scalability taking center stage, how do you see zero-knowledge proofs shifting the bottleneck in current DeFi protocols?",
      "I’ve been tracking fintech investments lately. Are you seeing major VC interest shifting toward scalable layer-2 chains, or is the focus still on layer-1 security?",
      "Hello! Since you're interested in decentralization, how are you approaching the trade-off between user experience and scalability in your current Web3 projects?"
    ],
    "feedback": null,
    "created_at": "2026-07-08T11:00:00.000Z"
  }
  ```

* **Error Responses**:
  - `400 Bad Request`: If description or interests are empty after stripping.
  - `422 Unprocessable Entity`: Field character length validation constraint failed.

---

## 3. Fact Verification Endpoints

### Verify Fact via Wikipedia
Queries Wikipedia APIs to search for topics/jargon and returns a brief summary and article URL.

* **URL**: `/api/facts/verify`
* **Method**: `POST`
* **Request Header**: `Content-Type: application/json`
* **Request Body**:
  | Field | Type | Required | Description |
  | :--- | :--- | :--- | :--- |
  | `topic` | `string` | Yes | Topic/term to check (2-100 chars). |

  *Example Payload:*
  ```json
  {
    "topic": "zero knowledge proof"
  }
  ```

* **Response (200 OK)**:
  ```json
  {
    "topic": "Zero-knowledge proof",
    "summary": "In cryptography, a zero-knowledge proof or zero-knowledge protocol is a method by which one party can prove to another party that a given statement is true...",
    "source_url": "https://en.wikipedia.org/wiki/Zero-knowledge_proof",
    "found": true
  }
  ```

---

## 4. History & Feedback Endpoints

### Fetch History
Retrieves all historical generated conversation sessions, sorted by date descending.

* **URL**: `/api/history`
* **Method**: `GET`
* **Query Parameters**:
  - `limit` (int, default `50`): Maximum history entries to return.
* **Response (200 OK)**:
  ```json
  [
    {
      "id": 12,
      "event_description": "Tech conference about Web3 scalability and Decentralized Finance.",
      "interests": "zero knowledge proofs, venture capital, fintech",
      "themes": ["Web3 Scalability", "Decentralized Finance", "Zero Knowledge Proofs"],
      "generated_starters": [ ... ],
      "feedback": "thumbs_up",
      "created_at": "2026-07-08T11:00:00.000Z"
    }
  ]
  ```

### Update Session Feedback
Rates a conversation session to help optimize future generations.

* **URL**: `/api/history/{session_id}/feedback`
* **Method**: `PUT`
* **Request Body**:
  | Field | Type | Required | Description |
  | :--- | :--- | :--- | :--- |
  | `feedback` | `string` | Yes | Must be `"thumbs_up"`, `"thumbs_down"`, or `""`. |

  *Example Payload:*
  ```json
  {
    "feedback": "thumbs_up"
  }
  ```

* **Response (200 OK)**: Returns the updated session object.
* **Error Responses**:
  - `400 Bad Request`: If feedback is not in the allowed values.
  - `404 Not Found`: Session ID does not exist in the database.
