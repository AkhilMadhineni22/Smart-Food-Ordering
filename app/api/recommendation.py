"""
API endpoints for menu recommendation 

"""
from fastapi import APIRouter,Depends
from app.config import get_settings
from app.services.recommendation_service import RecommendationService
from app.models.schemas import MenuRecommendationRequest, MenuRecommendationResponse
import os

router = APIRouter(prefix="/menu", tags=["Recommendation"])

def get_recommendation_service():
    settings = get_settings()
    model_path = os.path.join(settings.model_dir,"recommendation_model.keras")
    return RecommendationService(use_ai=settings.use_ai_models, model_path=model_path)

@router.post("/recommend", response_model=MenuRecommendationResponse)
async def recommend_menu_item(
    request: MenuRecommendationRequest,
    service : RecommendationService = Depends(get_recommendation_service)
):
    return service.recommend_item(request)