"""
API endpoints for cuisine classification
"""
from fastapi import APIRouter,Depends
from app.config import get_settings
from app.models.schemas import CuisineClassificationRequest, CuisineClassificationResponse
from app.services.cuisine_service import  CuisineService
import os

router = APIRouter(prefix="/restaurant", tags=["cuisine"])

def get_cuisine_service():
    "Dependancy to get cuisine service instance"
    settings = get_settings()
    return CuisineService(use_ai=settings.use_ai_models)

@router.post("/cuisine-classifier", response_model=CuisineClassificationResponse)
async def classify_cuisine(
    request: CuisineClassificationRequest,
    service: CuisineService = Depends(get_cuisine_service)
):
    
    return service.classify_cuisine(request)

