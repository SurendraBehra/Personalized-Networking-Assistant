import json
import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.schemas import StarterRequest, StarterResponse
from backend.services import ThemeExtractorInstance, TextGeneratorInstance, DBServiceInstance

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/starters",
    tags=["starters"]
)

@router.post("/generate", response_model=StarterResponse, status_code=status.HTTP_201_CREATED)
def generate_conversation_starters(payload: StarterRequest, db: Session = Depends(get_db)):
    """
    Generate professional conversation starters based on event description and interests.
    """
    event_desc = payload.event_description.strip()
    interests = payload.interests.strip()
    
    if not event_desc or not interests:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Event description and interests cannot be empty."
        )

    try:
        # Step 1: Extract core themes
        themes = ThemeExtractorInstance.extract_themes(event_desc, interests, api_key=payload.gemini_api_key)
        
        # Step 2: Retrieve positive feedback starters for few-shot learning
        few_shot = DBServiceInstance.get_positive_feedback_starters(db)
        
        # Step 3: Generate conversation starters
        starters = TextGeneratorInstance.generate_starters(
            event_desc, 
            interests, 
            themes, 
            few_shot, 
            api_key=payload.gemini_api_key
        )
        
        # Step 4: Save session in DB
        db_session = DBServiceInstance.save_session(
            db=db,
            event_description=event_desc,
            interests=interests,
            themes=themes,
            generated_starters=starters
        )
        
        # Prepare response model (deserialize JSON strings for pydantic)
        response_data = {
            "id": db_session.id,
            "event_description": db_session.event_description,
            "interests": db_session.interests,
            "themes": json.loads(db_session.themes),
            "generated_starters": json.loads(db_session.generated_starters),
            "feedback": db_session.feedback,
            "created_at": db_session.created_at
        }
        
        return response_data
    except Exception as e:
        logger.error(f"Error during starter generation endpoint execution: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while generating starters: {str(e)}"
        )
