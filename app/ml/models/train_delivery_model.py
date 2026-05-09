import pandas as pd
import mlflow
import mlflow.sklearn

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import mean_absolute_error, r2_score

# load dataset
df = pd.read_csv("C:/Users/Mahesh/Desktop/smart food ordering/app/data/Food_Delivery_Times.csv")

#clean data
df = df.dropna()
df = df.drop("Order_ID", axis=1)

#split the data
y = df["Delivery_Time_min"]
x = df.drop("Delivery_Time_min", axis=1)

categorical_cols = ["Weather", "Traffic_Level", "Time_of_Day", "Vehicle_Type"]
numerical_cols = ["Distance_km", "Preparation_Time_min", "Courier_Experience_yrs"]

preprocessor = ColumnTransformer([
    ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_cols),
    ("num", "passthrough", numerical_cols)
])

#full pipleine
pipeline = Pipeline([
    ("preprocessor", preprocessor),
    ("model", LogisticRegression())
])

#train test split
X_train, X_test, y_train, y_test = train_test_split(
    x, y, test_size=0.2, random_state=42
    )

# mlflow

mlflow.set_tracking_uri("file:./mlruns")
mlflow.set_experiment("Delivery Time model")
with mlflow.start_run():
    pipeline.fit(X_train,y_train)

    y_pred = pipeline.predict(X_test)

    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    mlflow.log_metric("mae",mae)
    mlflow.log_metric("r2",r2)

    mlflow.sklearn.log_model(pipeline, "model")

    print("MAE:", mae)
    print("R2:", r2)




