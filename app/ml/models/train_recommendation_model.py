import pandas as pd
import mlflow
import mlflow.keras
import pickle
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import tensorflow as tf
import random

menu = {
    "italian": ["pasta", "pizza", "lasagna", "garlic bread"],
    "indian": ["biryani", "butter chicken", "naan", "paneer curry"],
    "fast_food": ["burger", "fries", "sandwich"],
    "chinese": ["fried rice", "noodles", "manchurian"],
    "dessert": ["ice cream", "gulab jamun", "cake"],
    "drinks": ["coke", "pepsi", "juice"]
}

orders = []

for _ in range(5000):
    cuisine = random.choice(list(menu.keys()))
    main_items = random.sample(menu[cuisine],k = 2)
    order = main_items.copy()

    #add dessert sometimes
    if random.random() > 0.5:
        order.append(random.choice(menu["dessert"]))

    #add drinks sometimes
    if random.random() > 0.3:
        order.append(random.choice(menu["drinks"]))

    orders.append(order)

encoder = LabelEncoder()

all_items = [item for order in orders for item in order]
encoder.fit(all_items)

X, y = [], []

for order in orders:
    encoded = encoder.transform(order)

    for i in range(1, len(encoded)):
        X.append(encoded[:i])   # input sequence
        y.append(encoded[i])    # next item

# Pad sequences
X = tf.keras.preprocessing.sequence.pad_sequences(X, maxlen=5)
y = np.array(y)

vocab_size = len(encoder.classes_)
model = tf.keras.models.Sequential([
    
    tf.keras.layers.Embedding(input_dim=vocab_size, output_dim=32, input_length=5),
    
    tf.keras.layers.LSTM(32),
    
    tf.keras.layers.Dense(vocab_size, activation="softmax")
])

model.compile(
    optimizer = "adam",
    loss = "sparse_categorical_crossentropy",
    metrics = ["accuracy"]
)

model.fit(X, y, epochs=10)

#mlflow
mlflow.set_tracking_uri("file:./mlruns")
mlflow.set_experiment("Menu Recommendation model")

with mlflow.start_run() as run:

    # Log Keras model properly
    mlflow.keras.log_model(
        model,
        artifact_path="model",
        registered_model_name=None  # IMPORTANT: skip registry
    )

    # Save encoder
    with open("encoder.pkl", "wb") as f:
        pickle.dump(encoder, f)
    mlflow.log_artifact("encoder.pkl")

    # Save metadata
    metadata = {
        "max_len": 5,
        "vocab_size": vocab_size
    }
    with open("meta.pkl", "wb") as f:
        pickle.dump(metadata, f)
    mlflow.log_artifact("meta.pkl")

    print("Run ID:", run.info.run_id)