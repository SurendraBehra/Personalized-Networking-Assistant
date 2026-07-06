import json
import logging
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas import StarterResponse, FeedbackUpdateRequest
from ..services.db_service import DBServiceInstance

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/history",
    tags=["history"]
)

@router.get("", response_model=List[StarterResponse])
def get_history_endpoint(limit: int = 50, db: Session = Depends(get_db)):
    """
    Get recent conversation starters history.
    """
    try:
        sessions = DBServiceInstance.get_history(db, limit=limit)
        response_list = []
        for s in sessions:
            response_list.append({
                "id": s.id,
                "event_description": s.event_description,
                "interests": s.interests,
                "themes": json.loads(s.themes),
                "generated_starters": json.loads(s.generated_starters),
                "feedback": s.feedback,
                "created_at": s.created_at
            })
        return response_list
    except Exception as e:
        logger.error(f"Error fetching conversation history: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while fetching history: {str(e)}"
        )

@router.put("/{session_id}/feedback", response_model=StarterResponse)
def update_feedback_endpoint(
    session_id: int, 
    payload: FeedbackUpdateRequest, 
    db: Session = Depends(get_db)
):
    """
    Update feedback (thumbs_up, thumbs_down, or None) for a specific conversation session.
    """
    feedback_val = payload.feedback.strip() if payload.feedback else None
    
    if feedback_val and feedback_val not in ["thumbs_up", "thumbs_down"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Feedback must be either 'thumbs_up', 'thumbs_down', or empty."
        )

    try:
        updated_session = DBServiceInstance.update_feedback(db, session_id, feedback_val)
        if not updated_session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Conversation session with ID {session_id} not found."
            )
            
        return {
            "id": updated_session.id,
            "event_description": updated_session.event_description,
            "interests": updated_session.interests,
            "themes": json.loads(updated_session.themes),
            "generated_starters": json.loads(updated_session.generated_starters),
            "feedback": updated_session.feedback,
            "created_at": updated_session.created_at
        }
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Error updating feedback for session {session_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while updating feedback: {str(e)}"
        )
