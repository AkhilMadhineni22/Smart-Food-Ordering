"""
Centralized API client for backend communication
"""
import os
import sys
import requests
from dotenv import load_dotenv

# Load .env from frontend directory
env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
load_dotenv(env_path)

# Get API URL from environment or use default
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")


class APIClient:
    """Client for making requests to the FastAPI backend"""
    
    def __init__(self, base_url: str = API_BASE_URL):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})
    
    def _make_request(self, method: str, endpoint: str, data: dict = None):
        """Make HTTP request to backend"""
        url = f"{self.base_url}{endpoint}"
        try:
            if method.upper() == "POST":
                response = self.session.post(url, json=data)
            else:
                response = self.session.request(method, url)
            
            response.raise_for_status()
            return response.json()
        
        except requests.exceptions.ConnectionError:
            return {"error": "Cannot connect to backend. Make sure the server is running."}
        except requests.exceptions.HTTPError as e:
            return {"error": f"HTTP Error: {str(e)}"}
        except Exception as e:
            return {"error": str(e)}
    
    # Delivery Time API
    def predict_delivery_time(self, Distance_km: float, Weather: str, Traffic_Level: str,
                              Time_of_Day: str, Vehicle_Type: str, Preparation_Time_min: float,
                              Courier_Experience_yrs: float):
        data = {
        "Distance_km": float(Distance_km),
        "Weather": str(Weather),
        "Traffic_Level": str(Traffic_Level),
        "Time_of_Day": str(Time_of_Day),
        "Vehicle_Type": str(Vehicle_Type),
        "Preparation_Time_min": float(Preparation_Time_min),
        "Courier_Experience_yrs": float(Courier_Experience_yrs)
        }
        print(f"DEBUG: Sending data: {data}")  # Debug print
        return self._make_request("POST", "/order/delivery-time", data)
    
    # Menu Recommendation API
    def recommend_menu(self, past_orders: list):
        data = {"past_orders": past_orders}
        return self._make_request("POST", "/menu/recommend", data)
    
    # Review Classification API
    def classify_review(self, rating: float, review_text: str):
        data = {"rating": rating, "review_text": review_text}
        return self._make_request("POST", "/review/fake-or-real", data)
    
    # Cuisine Classification API
    def classify_cuisine(self, menu_items: str):
        data = {"menu_items": menu_items}
        return self._make_request("POST", "/restaurant/cuisine-classifier", data)
    
    # Smart Ticketing API
    def assign_ticket(self, issue_text: str):
        data = {"issue_text": issue_text}
        return self._make_request("POST", "/support/smart-ticketing", data)


# Create singleton instance
api_client = APIClient()