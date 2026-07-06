import logging
from fastapi import APIRouter, HTTPException, status
from ..schemas import FactSearchRequest, FactSearchResponse
from ..services.fact_verifier import FactVerifierInstance

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/facts",
    tags=["facts"]
)

@router.post("/verify", response_model=FactSearchResponse)
def verify_fact_endpoint(payload: FactSearchRequest):
    """
    Search Wikipedia for a topic and return a concise summary and source link.
    """
    topic = payload.topic.strip()
    if not topic:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Search topic cannot be empty."
        )

    try:
        result = FactVerifierInstance.verify_fact(topic)
        return result
    except Exception as e:
        logger.error(f"Error in fact verification endpoint: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while verifying the topic: {str(e)}"
        )
