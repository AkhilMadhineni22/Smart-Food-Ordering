"""
API endpoints for review classification
"""
from fastapi import APIRouter, Depends
from app.models.schemas import ReviewClassificationRequest, ReviewClassificationResponse
from app.services.review_service import ReviewService
from app.config import get_settings
import os

router = APIRouter(prefix="/review", tags=["Review"])

def get_review_service():
    """Dependency to get review service instance"""
    settings = get_settings()
    return ReviewService(use_ai=settings.use_ai_models)


@router.post("/fake-or-real", response_model=ReviewClassificationResponse)
async def classify_review(
    request: ReviewClassificationRequest,
    service: ReviewService = Depends(get_review_service)
):
  
    return service.classify_review(request)
