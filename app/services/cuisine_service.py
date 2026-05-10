"""
Service layer for cuisine classification
"""

from app.models.ml_models import CuisineClassifierModel
from app.models.schemas import CuisineClassificationRequest,CuisineClassificationResponse,CuisineType

class CuisineService:
    def __init__(self, use_ai: bool = False, model_path: str = None):
        self.model = CuisineClassifierModel(model_path=model_path)

    def classify_cuisine(self, request:CuisineClassificationRequest) -> CuisineClassificationResponse:
        """classify cuisine type based on menu items"""

        result = self.model.classify(request.menu_items)

        # Map model predictions to API enum values
        cuisine_mapping = {
            "Italian Recipes": "Italian",
            "North Indian Recipes": "Indian",
            "South Indian Recipes": "Indian",
            "Continental": "Continental",
            "Indian": "Indian",
            "Mexican": "Mexican"
        }

        mapped_cuisine = cuisine_mapping.get(result["cuisine"], result["cuisine"])

        return CuisineClassificationResponse (
            cuisine_type = CuisineType(mapped_cuisine),
            confidence_score = result["confidence"],
            model_used = result["model"],
             matched_keywords=result.get("matched_keywords")
        )
    