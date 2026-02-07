import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score
import joblib

# Load data
df = pd.read_csv("data/simulated_data.csv")
print(df.head())

# Features and target
X = df[["hour", "traffic_level", "rider_demand", "tariff_rs", "solar_kw"]]
y = df["wait_time_min"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
model = LinearRegression()
model.fit(X_train, y_train)

# Predict
y_pred = model.predict(X_test)

print("MAE:", mean_absolute_error(y_test, y_pred))
print("R2 Score:", r2_score(y_test, y_pred))

# SAVE MODEL
joblib.dump(model, "wait_time_model.pkl")
print("Model saved as wait_time_model.pkl")
