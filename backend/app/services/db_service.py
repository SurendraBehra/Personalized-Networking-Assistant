import json
import logging
from typing import List, Optional
from sqlalchemy.orm import Session
from ..models import ConversationStarterSession

logger = logging.getLogger(__name__)

class DBService:
    @staticmethod
    def save_session(
        db: Session, 
        event_description: str, 
        interests: str, 
        themes: List[str], 
        generated_starters: List[str]
    ) -> ConversationStarterSession:
        """
        Saves a generated conversation session to the database.
        """
        try:
            db_session = ConversationStarterSession(
                event_description=event_description,
                interests=interests,
                themes=json.dumps(themes),
                generated_starters=json.dumps(generated_starters),
                feedback=None
            )
            db.add(db_session)
            db.commit()
            db.refresh(db_session)
            return db_session
        except Exception as e:
            db.rollback()
            logger.error(f"Error saving conversation session: {e}")
            raise e

    @staticmethod
    def get_session_by_id(db: Session, session_id: int) -> Optional[ConversationStarterSession]:
        """
        Fetches a specific conversation session by its ID.
        """
        return db.query(ConversationStarterSession).filter(ConversationStarterSession.id == session_id).first()

    @staticmethod
    def update_feedback(db: Session, session_id: int, feedback: Optional[str]) -> Optional[ConversationStarterSession]:
        """
        Updates the feedback ('thumbs_up', 'thumbs_down', or None) of a specific session.
        """
        try:
            db_session = db.query(ConversationStarterSession).filter(ConversationStarterSession.id == session_id).first()
            if db_session:
                db_session.feedback = feedback
                db.commit()
                db.refresh(db_session)
                return db_session
            return None
        except Exception as e:
            db.rollback()
            logger.error(f"Error updating feedback for session {session_id}: {e}")
            raise e

    @staticmethod
    def get_history(db: Session, limit: int = 50) -> List[ConversationStarterSession]:
        """
        Fetches the recent conversation history, sorted by creation time descending.
        """
        return db.query(ConversationStarterSession).order_by(ConversationStarterSession.created_at.desc()).limit(limit).all()

    @staticmethod
    def get_positive_feedback_starters(db: Session, limit: int = 10) -> List[str]:
        """
        Retrieves generated conversation starters that received positive feedback ('thumbs_up').
        This will be used as few-shot training examples for future generations.
        """
        sessions = db.query(ConversationStarterSession).filter(
            ConversationStarterSession.feedback == 'thumbs_up'
        ).order_by(ConversationStarterSession.created_at.desc()).limit(limit).all()
        
        starters = []
        for s in sessions:
            try:
                # Parse the JSON list of starters and add them to our examples
                parsed = json.loads(s.generated_starters)
                if isinstance(parsed, list):
                    starters.extend(parsed)
            except Exception as e:
                logger.error(f"Error parsing starters for session {s.id}: {e}")
                
        # Return unique starters up to the limit
        return list(dict.fromkeys(starters))[:limit]

DBServiceInstance = DBService()
