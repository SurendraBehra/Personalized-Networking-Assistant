import unittest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from backend.app.main import app
from backend.database import Base, get_db
import backend.models as models

# Create an in-memory SQLite database for routing tests with StaticPool
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables in the in-memory database
Base.metadata.create_all(bind=engine)

# Override get_db dependency
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

class TestRouters(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        # Clear tables and re-create to keep tests isolated
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)

    def test_root_endpoint(self):
        """
        Test that root API endpoint returns status check info.
        """
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("message", response.json())
        self.assertEqual(response.json()["status"], "healthy")

    def test_generate_starters_validation_error(self):
        """
        Test that generating starters with empty input raises validation errors.
        """
        # Empty event description
        payload = {"event_description": "", "interests": "tech"}
        response = self.client.post("/api/starters/generate", json=payload)
        self.assertEqual(response.status_code, 422)  # Pydantic validation error

        # Empty body
        response = self.client.post("/api/starters/generate", json={})
        self.assertEqual(response.status_code, 422)

    def test_generate_starters_success_fallback(self):
        """
        Test generating starters returns response in fallback mode (when no API key is specified).
        """
        payload = {
            "event_description": "AI for Smart Cities Panel",
            "interests": "sustainability, climate change"
        }
        response = self.client.post("/api/starters/generate", json=payload)
        self.assertEqual(response.status_code, 201)
        data = response.json()
        
        self.assertIn("id", data)
        self.assertEqual(data["event_description"], "AI for Smart Cities Panel")
        self.assertEqual(data["interests"], "sustainability, climate change")
        self.assertIsInstance(data["themes"], list)
        self.assertTrue(len(data["themes"]) > 0)
        self.assertIsInstance(data["generated_starters"], list)
        self.assertEqual(len(data["generated_starters"]), 3)
        self.assertIsNone(data["feedback"])

    def test_get_history_and_feedback(self):
        """
        Test saving starters, checking the history list, and updating thumbs-up/thumbs-down feedback.
        """
        # 1. Generate starters to create a database session record
        payload = {
            "event_description": "General Networking Event",
            "interests": "entrepreneurship, VC"
        }
        gen_response = self.client.post("/api/starters/generate", json=payload)
        session_id = gen_response.json()["id"]

        # 2. Get history - check it shows in list
        hist_response = self.client.get("/api/history")
        self.assertEqual(hist_response.status_code, 200)
        history = hist_response.json()
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]["id"], session_id)
        self.assertIsNone(history[0]["feedback"])

        # 3. Update feedback to thumbs_up
        feed_response = self.client.put(f"/api/history/{session_id}/feedback", json={"feedback": "thumbs_up"})
        self.assertEqual(feed_response.status_code, 200)
        self.assertEqual(feed_response.json()["feedback"], "thumbs_up")

        # 4. Verify in history that it is updated
        hist_response2 = self.client.get("/api/history")
        self.assertEqual(hist_response2.json()[0]["feedback"], "thumbs_up")

        # 5. Invalid feedback validation
        feed_response_invalid = self.client.put(f"/api/history/{session_id}/feedback", json={"feedback": "invalid_val"})
        self.assertEqual(feed_response_invalid.status_code, 400)

if __name__ == '__main__':
    unittest.main()
