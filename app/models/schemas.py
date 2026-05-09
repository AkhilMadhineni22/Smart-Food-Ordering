"""
Pydantic models for API request and response validation
"""

from pydantic import BaseModel, validator, Field
from typing import List, Optional
from enum import Enum

class WeatherCondition(str,Enum):
    CLEAR = "Clear"
    RAINY = "Rainy"
    FOGGY = "Foggy"
    WINDY = "Windy"
    SNOWY = "Snowy"

class TrafficLevel(str,Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"

class VehicleType(str,Enum):
    SCOOTER = "Scooter"
    BIKE = "Bike"
    CAR = "Car"

class TimeOfTheDay(str,Enum):
    MORNING = "Morning"
    AFTERNOON = "Afternoon"
    EVENING = "Evening"
    NIGHT = "Night"

class CuisineType(str,Enum):
    INDIAN = "Indian"
    CHINESE = "Chinese"
    ITALIAN = "Italian"
    MEXICAN = "Mexican"
    CONTINENTAL = "Continental"
    ITALIAN_RECIPES = "Italian Recipes"
    NORTH_INDIAN_RECIPES = "North Indian Recipes"
    SOUTH_INDIAN_RECIPES = "South Indian Recipes"

class DeliveryTimeRequest(BaseModel):
    Distance_km: float = Field(..., gt=0, le=50, description="Distance in kilometers")
    Weather:WeatherCondition
    Traffic_Level:TrafficLevel
    Time_of_Day:TimeOfTheDay
    Vehicle_Type:VehicleType
    Preparation_Time_min:float = Field(..., gt=0, le=120, description="Restaurant preparation time in minutes")
    Courier_Experience_yrs: float = Field(..., ge=0, le=30, description="Courier experience in years")

class DeliveryTimeResponse(BaseModel):
    predicted_delivery_time_minutes: float
    model_used:str
    confidence:Optional[str] = None

class MenuRecommendationRequest(BaseModel):
    past_orders: List[str] = Field(..., min_length=1)

    @validator('past_orders')
    def validate_orders(cls, v):
        return [item.lower().strip() for item in v]
    
class MenuRecommendationResponse(BaseModel):
    recommended_item : str
    model_used:str
    confidence_score: float = Field(..., ge=0, le=1)
    reasoning: Optional[str] = None

class ReviewClassificationRequest(BaseModel):
    rating:float = Field(..., gt=0, le=5, description="Restaurant rating (1-5)")
    review_text:str = Field(..., min_length=1,max_length=1000)

class ReviewClassificationResponse(BaseModel):
    sentiment: str
    confidence: float = Field(..., ge=0, le=1)
    model: str
    reason: Optional[str] = None

class CuisineClassificationRequest(BaseModel):
    menu_items:str = Field(...,min_length=1)

    @validator('menu_items')
    def validate_menu_items(cls, v):
        # Split into words, not characters
        return v.lower().strip()
    
class CuisineClassificationResponse(BaseModel):
    cuisine_type:CuisineType
    model_used:str
    confidence_score:float = Field(..., gt=0,le=1)
    matched_keywords: Optional[List[str]] = None

class SmartTicketingRequest(BaseModel):
    issue_text:str = Field(..., min_length=1,max_length=1000)

class SmartTicketResponse(BaseModel):
    assigned_agent:str
    model_used:str
    agent_id:int
    confidence_score:float = Field(..., gt=0,le=1)
    reason:Optional[str] = None

class HealthResponse(BaseModel):
    status: str
    app_name: str
    version: str
    ai_models_loaded: bool    

 