import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text
from backend.database.connection import Base

class ConversationStarterSession(Base):
    __tablename__ = "conversation_sessions"

    id = Column(Integer, primary_key=True, index=True)
    event_description = Column(String(500), nullable=False)
    interests = Column(String(500), nullable=False)
    themes = Column(Text, nullable=False)  # JSON-serialized list of strings
    generated_starters = Column(Text, nullable=False)  # JSON-serialized list of strings
    feedback = Column(String(50), nullable=True)  # 'thumbs_up', 'thumbs_down', or None
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
