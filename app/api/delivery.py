"""
API endpoints for Delivery time prediction
"""
from fastapi import APIRouter, Depends
from app.config import get_settings
from app.models.schemas import DeliveryTimeRequest, DeliveryTimeResponse
from app.services.delivery_service import DeliveryService
import os

router = APIRouter(prefix= "/order", tags=["Delivery"])

def get_delivery_service ():
    settings = get_settings()
    model_path = os.path.join(settings.model_dir,"delivery_time_model.pkl")
    return DeliveryService(model_path=model_path, use_ai=settings.use_ai_models)

@router.post("/delivery-time", response_model=DeliveryTimeResponse)
async def predict_delivery_time(
    request:DeliveryTimeRequest,
    service:DeliveryService = Depends(get_delivery_service)
):
    return service.predict_delivery_time(request)