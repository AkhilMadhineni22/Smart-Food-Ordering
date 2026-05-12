import pickle
import numpy as np
import pandas as pd
from collections import Counter
from typing import Optional, List, Dict, Any
#from sentence_transformers import SentenceTransformer
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import tensorflow as tf
import joblib
import joblib

class DelivaryTimeModel:
    def __init__(self, model_path: Optional[str] = None):
        self.model = None
        self.is_ai = False
        if model_path:
            try:
                model = joblib.load(model_path)
                self.model = model
                self.is_ai = True
                print(" MLflow model loaded successfully")

            except Exception as e:
                print(" Failed to load MLflow model:", e)
                self.model = None
                    

    def predict(self, Distance_km: float, Weather: str, Traffic_Level: str,
                Time_of_Day: str, Vehicle_Type: str, Preparation_Time_min: float,
                Courier_Experience_yrs: float) -> Dict[str, Any]:
         if self.is_ai and self.model:
             input_data = pd.DataFrame([{
                 "Distance_km": Distance_km,
                 "Weather": Weather,
                 "Traffic_Level": Traffic_Level,
                 "Time_of_Day": Time_of_Day,
                 "Vehicle_Type": Vehicle_Type,
                 "Preparation_Time_min": Preparation_Time_min,
                 "Courier_Experience_yrs": Courier_Experience_yrs
             }])

             prediction = self.model.predict(input_data)[0]
             return {
                 "time":round(float(prediction),2),
                 "model": "ai"
             }
         #Rule based formula(fallback )
         base_time = Preparation_Time_min + (Distance_km * 3)

        # Weather impact
         weather_multiplier = {
                "Clear": 1.0, "Windy": 1.1, "Foggy": 1.2,
                "Rainy": 1.3, "Snowy": 1.5
            }
         base_time *= weather_multiplier.get(Weather, 1.0)

            # Traffic impact
         traffic_multiplier = {"Low": 1.0, "Medium": 1.25, "High": 1.5}
         base_time *= traffic_multiplier.get(Traffic_Level, 1.0)

            # Time of day impact
         if Time_of_Day in ["Evening", "Night"]:
                base_time *= 1.15

            # Vehicle type impact
         vehicle_multiplier = {"Bike": 0.85, "Scooter": 1.0, "Car": 1.1}
         base_time *= vehicle_multiplier.get(Vehicle_Type, 1.0)

            # Experienced couriers are faster
         if Courier_Experience_yrs >= 3:
                base_time *= 0.9
         elif Courier_Experience_yrs < 1:
                base_time *= 1.1

         return {"time": round(base_time, 2), "model": "basic"}

class RecommendationModel:
    def __init__(self, model_path: str = None):
        self.encoder = None
        self.meta = None
        self.is_ai = False
        self.model = None
        encoder_path = "app/ml/models/menu_recommendation_encoder.pkl"
        meta_path = "app/ml/models/meta.pkl"
        if model_path:
            try:
                self.model = tf.keras.models.load_model(model_path)
                with open(encoder_path, "rb") as f:
                    self.encoder = pickle.load(f)

                with open(meta_path, "rb") as f:
                    self.meta = pickle.load(f)
                    self.is_ai = True

                print(" Recommendation model loaded successfully")

            except Exception as e:
                print(" Failed to load model:", e)

    def recommend(self,past_orders:List[str]) -> Dict[str,any]:
         if self.is_ai and self.model and self.encoder:
              return self._ai_recommend(past_orders)
         else:
              counter = Counter(past_orders)
              most_common = counter.most_common(1)[0]
              return {
                "item": most_common[0],
                "confidence": round(most_common[1] / len(past_orders), 2),
                "model": "basic",
                "reasoning": f"Most frequently ordered ({most_common[1]} times)"
            }
         
    def _ai_recommend(self, past_orders: List[str]) -> Dict[str, any]:
        try:
            # Normalize input
            past_orders = [item.lower().strip() for item in past_orders]

            # Encode
            encoded = self.encoder.transform(past_orders)

            # Pad
            padded = tf.keras.preprocessing.sequence.pad_sequences([encoded], maxlen=5)

            # Predict
            probs = self.model.predict(padded)[0]

            predicted_index = np.argmax(probs)
            confidence = float(np.max(probs))

            predicted_item = self.encoder.inverse_transform([predicted_index])[0]

            return {
                "item": predicted_item,
                "confidence": round(confidence, 2),
                "model": "ai",
                "reasoning": "Predicted next likely item based on order sequence"
            }

        except Exception as e:
            print("Prediction error:", e)

            return {
                "item": past_orders[-1],
                "confidence": 0.5,
                "model": "basic",
                "reasoning": "Fallback due to prediction error"
            }

class ReviewClassifierModel:
    def __init__(self, model_path: str = None):
        self.model = None
        self.is_ai = False
        if model_path:
            try:
               self.model = joblib.load(model_path)
               self.is_ai = True
               print(" Review model loaded")
            except Exception as e:
                print("Error loading review classifier model:", e)

    def classify(self, rating:float, review_text:str) -> Dict[str,any]:
        if self.is_ai and self.model:
            prediction = self.model.predict([review_text])[0]

            prob = self.model.predict_proba([review_text])[0]
            confidence_score = max(prob)
            # is_genuine = True if prediction == "Positive" else False

            return{
                "sentiment": prediction,
                "confidence":round(float(confidence_score),2),
                "model": "ai"
            }
        
        # Basic rule-based classification (DO NOT MODIFY - this is the fallback)
        is_genuine = True
        confidence = 0.7
        reason = "Normal review"
        
        if len(review_text.split()) < 5:
            is_genuine = False
            confidence = 0.8
            reason = "Too short"
        elif review_text.count('!') > 5:
            is_genuine = False
            confidence = 0.75
            reason = "Too many exclamations"
        elif "best ever" in review_text.lower():
            is_genuine = False
            confidence = 0.7
            reason = "Generic superlatives"
        elif rating == 5 and len(review_text.split()) < 10:
            is_genuine = False
            confidence = 0.65
            reason = "Perfect rating with very short review"
        elif rating <= 1 and len(review_text.split()) < 10:
            is_genuine = False
            confidence = 0.65
            reason = "Extreme low rating with very short review"
        
        return {
            "is_genuine": is_genuine,
            "confidence": confidence,
            "model": "basic",
            "reason": reason
        }
    
class CuisineClassifierModel:
    KEYWORDS = {
        "Italian": ["pasta", "pizza", "risotto", "lasagna", "parmesan"],
        "Indian": ["curry", "masala", "naan", "tandoori", "biryani", "paneer"],
        "Chinese": ["noodles", "dumplings", "soy sauce", "wonton", "kung pao"],
        "Mexican": ["taco", "burrito", "salsa", "quesadilla", "guacamole"],
        "Japanese": ["sushi", "ramen", "tempura", "miso", "teriyaki"],
        "Thai": ["pad thai", "coconut", "lemongrass", "green curry", "peanut"],
        "American": ["burger", "fries", "bbq", "steak", "hot dog"],
        "Mediterranean": ["hummus", "falafel", "pita", "tzatziki", "tabbouleh"]
    }

    def __init__(self, model_path: str = None):
        self.is_ai = False
        self.vectorizer = None
        self.model = None
        if model_path:
            try:
                self.model = joblib.load(model_path)
                self.is_ai = True
                print(" Cuisine model loaded")

            except Exception as e:
                print(f"Warning: Failed to load cuisine model: {e}")
                self.is_ai = False

    def classify(self, menu_items) -> Dict[str, any]:
        # Handle both string and list inputs
        if isinstance(menu_items, str):
            text = menu_items
        else:
            text = " ".join(menu_items)
        
        if self.is_ai and self.model:
            prediction = self.model.predict([text])[0]

            try:
                confidence = self.model.predict_proba([text])[0]
                confidence_score = float(max(confidence))
            except Exception:
                confidence_score = 1.0

            return {
                "cuisine": str(prediction),
                "confidence": round(float(confidence_score), 2),
                "model": "ai"
            }
        
        # Basic keyword matching (DO NOT MODIFY - this is the fallback)
        # Handle both string and list inputs for fallback logic
        if isinstance(menu_items, str):
            items = menu_items.lower().split()
        else:
            items = menu_items
        
        scores = {cuisine: 0 for cuisine in self.KEYWORDS.keys()}
        matched = {cuisine: [] for cuisine in self.KEYWORDS.keys()}
        
        for item in items:
            item_lower = item.lower()
            for cuisine, keywords in self.KEYWORDS.items():
                for keyword in keywords:
                    if keyword in item_lower:
                        scores[cuisine] += 1
                        matched[cuisine].append(keyword)
        
        best_cuisine = max(scores, key=scores.get)
        total_matches = sum(scores.values())
        confidence = scores[best_cuisine] / total_matches if total_matches > 0 else 0.5
        
        return {
            "cuisine": best_cuisine,
            "confidence": round(confidence, 2),
            "model": "basic",
            "matched_keywords": list(set(matched[best_cuisine]))
        }
    
class TicketAssignmentModel:
    def __init__(self):
        from app.config import get_settings
        settings = get_settings()

        self.use_ai = False
        self.embedding_model = None
        self.reason_model = None
        self.agents = []

    def assign(self, issue_text: str):
        if self.use_ai and self.embedding_model is None:
            try:
                self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
                print("Embedding model loaded successfully")
            except Exception as e:
                print(f"Embedding model failed: {e}")
                return self._basic_assign(issue_text)

        if not self.use_ai or self.embedding_model is None:
            return self._basic_assign(issue_text)
        
        ticket_embedding = self.embedding_model.encode([issue_text])

        best_agent = None
        best_score = -1

        for agent in self.agents:
            skill_embedding = self.embedding_model.encode([agent["skills"]])

            similarity = cosine_similarity(
                ticket_embedding,
                skill_embedding
            )[0][0]

            experience_score = agent["experience"] / 5
            workload_penalty = agent["current_tickets"] / 10

            final_score = (
                0.6 * similarity +
                0.3 * experience_score -
                0.1 * workload_penalty
            )

            # Normalize score to 0-1 range
            final_score = max(0, min(1, final_score))

            if final_score > best_score:
                best_score = final_score
                best_agent = agent

        reason = self.generate_reason(issue_text, best_agent,best_score)

        return {
            "assigned_agent": best_agent["name"],
            "agent_id": best_agent["id"],
            "confidence_score": float(best_score),
            "model_used": "ai",
            "reason": reason
        }

    def _basic_assign(self, issue_text: str):
        """Basic assignment using keyword matching"""
        issue_lower = issue_text.lower()
        issue_words = set(issue_lower.split())

        # Simple keyword matching for agent skills
        keyword_scores = {}
        for agent in self.agents:
            score = 0
            skills_lower = agent["skills"].lower()
            # Count matching keywords
            for word in issue_words:
                if word in skills_lower:
                    score += 1
            keyword_scores[agent["id"]] = score / len(issue_words) if issue_words else 0  # Normalize by issue length

        # Find best agent by keyword match, then by experience
        best_agent = None
        best_score = -1

        for agent in self.agents:
            keyword_score = keyword_scores.get(agent["id"], 0)
            experience_score = agent["experience"] / 5
            workload_penalty = agent["current_tickets"] / 10

            final_score = (
                0.5 * keyword_score +
                0.3 * experience_score -
                0.2 * workload_penalty
            )

            # Normalize score to 0-1 range
            final_score = max(0, min(1, final_score))

            if final_score > best_score:
                best_score = final_score
                best_agent = agent

        reason = f"Basic keyword matching - agent has relevant skills for this issue"

        return {
            "assigned_agent": best_agent["name"],
            "agent_id": best_agent["id"],
            "confidence_score": float(best_score),
            "model_used": "basic",
            "reason": reason
        }

    def generate_reason(self, issue_text: str, agent: dict, similarity_score=None):
        ticket_lower = issue_text.lower()
        skills = agent["skills"]

    # ---- Step 1: Detect issue type ----
        if any(word in ticket_lower for word in ["refund", "charged", "payment", "billing"]):
            issue_type = "payment-related issue"
        elif any(word in ticket_lower for word in ["late", "delivery", "address"]):
            issue_type = "delivery-related issue"
        elif any(word in ticket_lower for word in ["missing", "wrong order", "food"]):
            issue_type = "order accuracy issue"
        elif any(word in ticket_lower for word in ["login", "account", "error", "bug"]):
            issue_type = "technical issue"
        else:
            issue_type = "general customer issue"

        # ---- Step 2: Extract matched skills ----
        matched_keywords = []
        for word in ticket_lower.split():
            if word in skills.lower():
                matched_keywords.append(word)

        matched_keywords = list(set(matched_keywords))

        # ---- Step 3: Experience + workload ----
        experience = agent["experience"]
        workload = agent["current_tickets"]

        if experience >= 4:
            exp_text = "highly experienced"
        elif experience >= 2:
            exp_text = "moderately experienced"
        else:
            exp_text = "less experienced"

        if workload <= 2:
            load_text = "low current workload"
        elif workload <= 5:
            load_text = "manageable workload"
        else:
            load_text = "high workload"

        # ---- Step 4: Build reasoning ----
        reason = f"This issue was identified as a {issue_type}. "

        if matched_keywords:
            reason += f"The agent has relevant expertise in {', '.join(matched_keywords)}. "
        else:
            reason += f"The agent's skillset ({skills}) aligns well with this type of issue. "

        reason += f"They are {exp_text} and currently have a {load_text}, making them a suitable choice."

        # Optional: add confidence hint
        if similarity_score:
            if similarity_score > 0.8:
                reason += " This is a strong match."
            elif similarity_score > 0.6:
                reason += " This is a good match."

        return reason