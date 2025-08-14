"""import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix

# Load dataset
df = pd.read_csv('updat_sensor_data.csv')  # replace with your file path

# EDA
print("Dataset Info:")
print(df.info())

print("\nMissing Values:")
print(df.isnull().sum())

print("\nClass Distribution:")
print(df['blockage_status'].value_counts())

# Convert timestamp to datetime if needed
df['timestamp'] = pd.to_datetime(df['timestamp'], dayfirst=True)

# Drop timestamp for training (optional: keep for reference)
df.drop(['timestamp'], axis=1, inplace=True)

# Encode location column
df['location'] = df['location'].astype('category').cat.codes

# Separate features and target
X = df.drop('blockage_status', axis=1)
y = df['blockage_status']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train Random Forest model
rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)

# Predictions and evaluation
y_pred = rf.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"\nAccuracy: {accuracy:.2f}")
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

print("\nAccuracy:", round(accuracy, 2))
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# ✅ Save the trained model

joblib.dump(rf_model, 'blockage_rf_model.pkl')
print("✅ Model saved successfully as 'blockage_rf_model.pkl'")
# Confusion Matrix
conf_matrix = confusion_matrix(y_test, y_pred)
sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues')
plt.title('Confusion Matrix')
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.show()

# Feature Importance Plot
importances = rf.feature_importances_
features = X.columns
indices = np.argsort(importances)[::-1]

plt.figure(figsize=(10, 6))
plt.title("Feature Importances")
plt.bar(range(X.shape[1]), importances[indices], align="center")
plt.xticks(range(X.shape[1]), [features[i] for i in indices], rotation=90)
plt.tight_layout()
plt.show()
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix

# Load dataset
df = pd.read_csv('updat_sensor_data.csv')  # replace with your actual file path

# Display dataset info
print("Dataset Info:")
print(df.info())

print("\nMissing Values:")
print(df.isnull().sum())

print("\nClass Distribution:")
print(df['blockage_status'].value_counts())

# Convert timestamp to datetime
df['timestamp'] = pd.to_datetime(df['timestamp'], dayfirst=True)

# Drop timestamp (not used for training)
df.drop(['timestamp'], axis=1, inplace=True)

# Encode location column
df['location'] = df['location'].astype('category').cat.codes

# Separate features and target
X = df.drop('blockage_status', axis=1)
y = df['blockage_status']

# Split data into train and test sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train Random Forest model (with class balancing)
rf = RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced')
rf.fit(X_train, y_train)

# Predict on test set
y_pred = rf.predict(X_test)

# Evaluate model
accuracy = accuracy_score(y_test, y_pred)
print(f"\n✅ Accuracy: {accuracy:.2f}")
print("\n✅ Classification Report:")
print(classification_report(y_test, y_pred))

# Save the trained model
joblib.dump(rf, 'models/blockage_rf_model.pkl')
print("\n✅ Model saved successfully as 'blockage_rf_model.pkl'")

# Plot confusion matrix
conf_matrix = confusion_matrix(y_test, y_pred)
sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues')
plt.title('Confusion Matrix')
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.show()

# Plot feature importances
importances = rf.feature_importances_
features = X.columns
indices = np.argsort(importances)[::-1]

plt.figure(figsize=(10, 6))
plt.title("Feature Importances")
plt.bar(range(X.shape[1]), importances[indices], align="center")
plt.xticks(range(X.shape[1]), [features[i] for i in indices], rotation=90)
plt.tight_layout()
plt.show()
