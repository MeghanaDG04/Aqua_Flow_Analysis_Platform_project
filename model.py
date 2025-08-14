"""import joblib
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from xgboost import XGBClassifier

# Load dataset
dataset_path = "merged_sensor_data.csv"
df = pd.read_csv(dataset_path)

# Handle missing values
df.fillna(df.mean(numeric_only=True), inplace=True)

# Define target column
target_column = "blockage_status"
X = df.drop(columns=["timestamp", "location", target_column])
y = df[target_column]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Standardize numerical features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train XGBoost model
xgb_model = XGBClassifier()
xgb_model.fit(X_train_scaled, y_train)

# Save trained model and scaler
joblib.dump(xgb_model, "xgboost_model.pkl")  # Save model
joblib.dump(scaler, "scaler.pkl")  # Save scaler

print("✅ Model and Scaler Saved Successfully!")
"""
import joblib

# Save the trained model to a .pkl file
joblib.dump(rf_model, 'models/blockage_rf_model.pkl')

print("✅ Model saved successfully as 'blockage_rf_model.pkl'")
