"""
Service layer for Delivery time prediction
"""
from app.models.ml_models import DelivaryTimeModel
from app.models.schemas import DeliveryTimeRequest, DeliveryTimeResponse

class DeliveryService:
    def __init__(self, model_path: str, use_ai: bool = True):
        self.model = DelivaryTimeModel(model_path=model_path)

    def predict_delivery_time(self,request:DeliveryTimeRequest) -> DeliveryTimeResponse:
        "Predict delivery time based on input features"

        result = self.model.predict(
            Distance_km=request.Distance_km,
            Weather=request.Weather.value,
            Traffic_Level=request.Traffic_Level.value,
            Time_of_Day=request.Time_of_Day.value,
            Vehicle_Type=request.Vehicle_Type.value,
            Preparation_Time_min=request.Preparation_Time_min,
            Courier_Experience_yrs=request.Courier_Experience_yrs
        )

        return DeliveryTimeResponse(
            predicted_delivery_time_minutes = result["time"],
            model_used=result["model"],
            confidence="High" if result["model"] == "ai" else "Medium"
        )
        