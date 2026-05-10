"""
service layer for Review Classifier
"""

from app.models.ml_models import ReviewClassifierModel
from app.models.schemas import ReviewClassificationRequest, ReviewClassificationResponse

class ReviewService:
    def __init__(self, use_ai: bool = True, model_path: str = None):
        self.model = ReviewClassifierModel(model_path=model_path)

    def classify_review(self, request:ReviewClassificationRequest) -> ReviewClassificationResponse:
        """Classify if review is genuine or fake"""
        result = self.model.classify(
            rating = request.rating,
            review_text = request.review_text
        ) 

        return ReviewClassificationResponse(
            sentiment=result["sentiment"],
            confidence=result["confidence"],
            model=result["model"],
            reason=result.get("reason")
        )
    
    
