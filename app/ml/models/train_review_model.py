import pandas as pd
import mlflow
import mlflow.sklearn

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score


#load the data
df = pd.read_csv("C:/Users/Mahesh/Desktop/smart food ordering/app/data/Restaurant_Reviews.tsv",sep="\t")

#clean data
df["sentiment"] = df["Liked"].apply(lambda x: "Positive" if x == 1 else "Negative")

#split data
x = df["Review"]
y = df["sentiment"]

x_train,x_test,y_train,y_test = train_test_split(
    x,y, test_size = 0.2, random_state = 42
)

#build pipeline
pipeline = Pipeline([
      ("tfidf", TfidfVectorizer(stop_words="english")),
    ("model", RandomForestClassifier(
        n_estimators=200,
        max_depth=20,
        random_state=42,
        min_samples_split=10,
        min_samples_leaf=2,
        max_features="sqrt",
    ))
])

pipeline.fit(x_train,y_train)

#evaluate

y_pred = pipeline.predict(x_test)

accuracy = accuracy_score(y_test,y_pred)
report = classification_report(y_test,y_pred,output_dict=True)

#mlflow

mlflow.set_tracking_uri("file:./mlruns")
mlflow.set_experiment("Review Classification model")

with mlflow.start_run():
    mlflow.log_metric("accuracy", accuracy)
    mlflow.log_param("model", "RandomForest"+"TFIDF")
    
    for label in ["Positive", "Negative"]:
        mlflow.log_metric(f"{label}_precision", report[label]["precision"])
        mlflow.log_metric(f"{label}_recall", report[label]["recall"])
        mlflow.log_metric(f"{label}_f1", report[label]["f1-score"])

    # Macro / weighted
    mlflow.log_metric("macro_f1", report["macro avg"]["f1-score"])
    mlflow.log_metric("weighted_f1", report["weighted avg"]["f1-score"])
    
    mlflow.sklearn.log_model(pipeline,"model")

print("model logged to ml flow")
