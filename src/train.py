import pandas as pd
import joblib
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    roc_auc_score,
    RocCurveDisplay
)

from feature_extractor import extract_features


print("Loading large dataset...")

data = pd.read_csv("../data/guardianai_large_dataset.csv")

print("Total rows:", len(data))

# -----------------------------
# Feature Extraction
# -----------------------------
print("Extracting features...")

X_features = []
for url in data['url']:
    X_features.append(extract_features(str(url)))

X = pd.DataFrame(X_features)
y = data['label']

# -----------------------------
# Train/Test Split (STRATIFIED)
# -----------------------------
print("Splitting dataset...")

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y   # Important for balanced split
)

# -----------------------------
# Train Model (Anti-Overfitting Settings)
# -----------------------------
print("Training model...")

model = RandomForestClassifier(
    n_estimators=200,
    max_depth=15,
    min_samples_split=5,
    min_samples_leaf=2,
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)

# -----------------------------
# Evaluation
# -----------------------------
print("Evaluating...")

predictions = model.predict(X_test)
probabilities = model.predict_proba(X_test)[:, 1]

print("\nClassification Report:")
print(classification_report(y_test, predictions))

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, predictions))

auc_score = roc_auc_score(y_test, probabilities)
print("\nROC AUC Score:", auc_score)

# -----------------------------
# Cross Validation (ROC AUC Based)
# -----------------------------
cv_scores = cross_val_score(
    model,
    X,
    y,
    cv=5,
    scoring='roc_auc'
)

print("\n5-Fold Cross Validation ROC-AUC:", cv_scores.mean())

# -----------------------------
# Feature Importance (Top 10)
# -----------------------------
importances = model.feature_importances_
feature_names = X.columns

importance_df = pd.DataFrame({
    "Feature": feature_names,
    "Importance": importances
}).sort_values(by="Importance", ascending=False)

print("\nTop 10 Important Features:")
print(importance_df.head(10))

# -----------------------------
# Save Model
# -----------------------------
joblib.dump(model, "../models/phishing_model.pkl")
print("\nModel saved successfully.")

# -----------------------------
# ROC Curve Plot
# -----------------------------
RocCurveDisplay.from_estimator(model, X_test, y_test)
plt.title("GuardianAI ROC Curve")
plt.show()