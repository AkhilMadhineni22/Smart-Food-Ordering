# Smart Food Ordering System

## Overview
The Smart Food Ordering System is an AI-powered application that integrates multiple machine learning models to enhance different aspects of a food ordering platform. It provides intelligent predictions, recommendations, and automation across delivery, menu suggestions, review analysis, cuisine detection, and support ticket routing.

This project demonstrates an end-to-end AI system with frontend, backend, and MLOps integration.

---

## Features

### 1. Delivery Time Prediction
Predicts the estimated delivery time based on multiple factors such as:
- Distance
- Weather conditions
- Traffic levels
- Time of day
- Vehicle type
- Preparation time
- Courier experience

Uses a trained machine learning model with a rule-based fallback.

---

### 2. Menu Recommendation System
Suggests the next food item based on the current order using a sequence-based deep learning model (LSTM).

- Learns ordering patterns
- Provides next-item recommendations
- Uses encoder + sequence padding + neural network

---

### 3. Review Classification
Classifies customer reviews as genuine or suspicious using NLP techniques.

- TF-IDF vectorization
- Random Forest classifier
- Confidence scoring
- Rule-based fallback for edge cases

---

### 4. Cuisine Classifier
Identifies the cuisine type based on food names, descriptions, and ingredients.

- TF-IDF with n-grams
- MLP classifier
- Handles multiple cuisine categories
- Filters low-frequency classes for better accuracy

---

### 5. Support Ticket Routing
Automatically assigns customer issues to the most relevant support agent.

- Uses sentence embeddings for semantic similarity
- Scores agents based on:
  - Skill relevance
  - Experience
  - Current workload
- Generates reasoning for assignment

---

## Tech Stack

### Backend
- FastAPI
- Python

### Frontend
- Streamlit

### Machine Learning
- Scikit-learn
- TensorFlow / Keras
- Sentence Transformers

### MLOps
- MLflow (experiment tracking, model logging)

---

## Project Structure
smart-food-ordering/
│
├── app/
│ ├── api/
│ ├── models/
│ ├── services/
│ └── config/
│
├── frontend/
│ ├── pages/
│ └── components/
│
├── mlruns/ # MLflow tracking data
├── requirements.txt
├── README.md


## Conclusion

This project demonstrates a complete AI application lifecycle including:
- Data processing
- Model training
- API development
- Frontend integration
- MLOps practices

It is designed to be modular, extensible, and production-ready with further enhancements.

Note: The semantic ticket assignment model using SentenceTransformers was disabled in the deployed cloud version due to memory limitations of the Render free-tier infrastructure.
Note: The deployed backend may take a few seconds to respond initially due to Render free-tier cold starts.
