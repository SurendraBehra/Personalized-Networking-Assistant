from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class StarterRequest(BaseModel):
    event_description: str = Field(..., min_length=3, max_length=500, description="Description of the networking event")
    interests: str = Field(..., min_length=3, max_length=500, description="User's professional or social interests")
    gemini_api_key: Optional[str] = Field(None, description="Optional custom Gemini API Key passed from the frontend")


class StarterResponse(BaseModel):
    id: int
    event_description: str
    interests: str
    themes: List[str]
    generated_starters: List[str]
    feedback: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

class FeedbackUpdateRequest(BaseModel):
    feedback: str = Field(..., description="Must be 'thumbs_up', 'thumbs_down', or null")

class FactSearchRequest(BaseModel):
    topic: str = Field(..., min_length=2, max_length=100, description="The topic to search on Wikipedia")

class FactSearchResponse(BaseModel):
    topic: str
    summary: str
    source_url: Optional[str] = None
    found: bool
