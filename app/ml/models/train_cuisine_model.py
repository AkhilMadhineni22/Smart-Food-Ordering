import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import classification_report, accuracy_score
import mlflow
import mlflow.sklearn

#load the data
df = pd.read_csv("C:/Users/Mahesh/Desktop/smart food ordering/app/data/Food_Recipe.csv")

#clean data
df = df.dropna(subset = ["name", "cuisine"])
cuisine_counts = df["cuisine"].value_counts()

valid_cuisines = cuisine_counts[cuisine_counts >= 20].index

df = df[df["cuisine"].isin(valid_cuisines)]

#prepare data
x = df["name"]+ " " +df["description"]+ " " +df["ingredients_name"]
y = df["cuisine"]

x_train, x_test, y_train, y_test  = train_test_split(
    x,y, test_size = 0.2, random_state = 42
)

#build pipeline
pipeline = Pipeline([
    ("tfidf", TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2),
        max_features=5000
    )),
    ("model", MLPClassifier(
        hidden_layer_sizes=(128, 64),
        activation="relu",
        solver="adam",
        max_iter=500,
        random_state=42
    ))
])

#mlflow
mlflow.set_tracking_uri("file:./mlruns")
mlflow.set_experiment("Cuisine Classification model")
with mlflow.start_run() as run:
    print("Training Cuisine Classification model...")
    pipeline.fit(x_train,y_train)

    y_pred = pipeline.predict(x_test)
    acc = accuracy_score(y_test,y_pred)
    report = classification_report(y_test,y_pred,output_dict=True)

    print("Accuracy:", acc)
    print("Classification Report:", report)

    mlflow.log_metric("accuracy", acc)
    mlflow.log_param("model_type", "MLPClassifier")
    mlflow.log_param("max_features", 5000)
    mlflow.log_param("ngram_range", "(1,2)")
    mlflow.log_param("hidden_layers", "(128,64)")
    mlflow.log_param("activation", "relu")
    mlflow.log_param("solver", "adam")
    mlflow.log_param("test_size", 0.2)

    for label, metrics in report.items():
        if isinstance(metrics, dict):
            mlflow.log_metric(f"{label}_precision", metrics.get("precision", 0))
            mlflow.log_metric(f"{label}_recall", metrics.get("recall", 0))
            mlflow.log_metric(f"{label}_f1", metrics.get("f1-score", 0))

    mlflow.sklearn.log_model(pipeline, "model")
    print("\n Model logged to MLflow!")
    print(f" Run ID: {run.info.run_id}")




