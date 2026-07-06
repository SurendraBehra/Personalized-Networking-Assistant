import unittest
import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.app.database import Base
from backend.app.services.db_service import DBServiceInstance
from backend.app.models import ConversationStarterSession

# Setup an in-memory SQLite engine and session factory for testing
engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class TestDBService(unittest.TestCase):
    def setUp(self):
        # Create all tables before each test
        Base.metadata.create_all(bind=engine)
        self.db = TestingSessionLocal()

    def tearDown(self):
        # Close session and drop tables after each test
        self.db.close()
        Base.metadata.drop_all(bind=engine)

    def test_save_and_retrieve_session(self):
        """
        Test that DBService correctly saves a conversation session and can retrieve it.
        """
        event_desc = "AI and Humanity Symposium"
        interests = "ethics, philosophy, NLP"
        themes = ["AI Ethics", "Humanity", "Philosophy"]
        starters = ["Question 1", "Question 2", "Question 3"]

        # Save session
        session = DBServiceInstance.save_session(
            db=self.db,
            event_description=event_desc,
            interests=interests,
            themes=themes,
            generated_starters=starters
        )

        self.assertIsNotNone(session.id)
        self.assertEqual(session.event_description, event_desc)
        self.assertEqual(session.interests, interests)
        self.assertEqual(json.loads(session.themes), themes)
        self.assertEqual(json.loads(session.generated_starters), starters)
        self.assertIsNone(session.feedback)

        # Retrieve session
        fetched = DBServiceInstance.get_session_by_id(self.db, session.id)
        self.assertIsNotNone(fetched)
        self.assertEqual(fetched.id, session.id)
        self.assertEqual(fetched.event_description, event_desc)

    def test_update_feedback(self):
        """
        Test that DBService can update feedback on a session.
        """
        session = DBServiceInstance.save_session(
            db=self.db,
            event_description="Networking Event",
            interests="VC, tech",
            themes=["VC"],
            generated_starters=["Starter 1"]
        )
        
        # Initial feedback is None
        self.assertIsNone(session.feedback)

        # Update feedback to thumbs_up
        updated = DBServiceInstance.update_feedback(self.db, session.id, "thumbs_up")
        self.assertIsNotNone(updated)
        self.assertEqual(updated.feedback, "thumbs_up")

        # Update feedback to thumbs_down
        updated2 = DBServiceInstance.update_feedback(self.db, session.id, "thumbs_down")
        self.assertEqual(updated2.feedback, "thumbs_down")

    def test_get_history_ordering(self):
        """
        Test that get_history returns sessions in descending chronological order.
        """
        # Save two sessions
        DBServiceInstance.save_session(self.db, "Event A", "Int A", ["Theme A"], ["Starter A"])
        DBServiceInstance.save_session(self.db, "Event B", "Int B", ["Theme B"], ["Starter B"])

        history = DBServiceInstance.get_history(self.db)
        self.assertEqual(len(history), 2)
        # Event B was saved second, so it should be first in descending order
        self.assertEqual(history[0].event_description, "Event B")
        self.assertEqual(history[1].event_description, "Event A")

    def test_get_positive_feedback_starters(self):
        """
        Test retrieving highly-rated conversation starters for few-shot examples.
        """
        # Session 1: thumbs_up
        s1 = DBServiceInstance.save_session(self.db, "Event 1", "Int 1", ["T1"], ["S1-1", "S1-2"])
        DBServiceInstance.update_feedback(self.db, s1.id, "thumbs_up")

        # Session 2: thumbs_down (should not be retrieved)
        s2 = DBServiceInstance.save_session(self.db, "Event 2", "Int 2", ["T2"], ["S2-1"])
        DBServiceInstance.update_feedback(self.db, s2.id, "thumbs_down")

        # Session 3: thumbs_up
        s3 = DBServiceInstance.save_session(self.db, "Event 3", "Int 3", ["T3"], ["S3-1", "S1-1"]) # S1-1 is duplicate
        DBServiceInstance.update_feedback(self.db, s3.id, "thumbs_up")

        positive_starters = DBServiceInstance.get_positive_feedback_starters(self.db, limit=5)
        
        # Should contain starters from s1 and s3, and duplicates should be filtered out
        self.assertEqual(len(positive_starters), 3)
        self.assertIn("S1-1", positive_starters)
        self.assertIn("S1-2", positive_starters)
        self.assertIn("S3-1", positive_starters)
        self.assertNotIn("S2-1", positive_starters) # From the thumbs_down session

if __name__ == "__main__":
    unittest.main()
