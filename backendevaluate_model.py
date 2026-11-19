import os
import pandas as pd

from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.ensemble import RandomForestClassifier

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASET_PATH = os.path.join(BASE_DIR, "dataset", "dataset.csv")

# Load dataset
data = pd.read_csv(DATASET_PATH)

data.columns = data.columns.str.strip()

X_raw = data.drop(columns=["Disease"])
y = data["Disease"].astype(str).str.strip()

# Clean symptoms
X_raw = X_raw.fillna("")
X_raw = X_raw.astype(str).apply(
    lambda col: col.str.strip().str.lower()
)

# Create symptom list
all_symptoms = sorted({
    value
    for value in X_raw.to_numpy().flatten()
    if value and value != "nan"
})

# Binary symptom matrix
X = pd.DataFrame(0, index=data.index, columns=all_symptoms)

for column in X_raw.columns:
    for index, symptom in X_raw[column].items():
        if symptom and symptom != "nan":
            X.at[index, symptom] = 1

# Remove duplicate patterns
X["Disease"] = y
combined = X.drop_duplicates()

y = combined["Disease"]
X = combined.drop(columns=["Disease"])

print("Unique records:", len(X))
print("Number of diseases:", y.nunique())

# Five-fold cross-validation
cv = StratifiedKFold(
    n_splits=5,
    shuffle=True,
    random_state=42
)

model = RandomForestClassifier(
    n_estimators=200,
    random_state=42,
    class_weight="balanced"
)

scores = cross_val_score(
    model,
    X,
    y,
    cv=cv,
    scoring="accuracy"
)

print("\n========== 5-FOLD CROSS VALIDATION ==========")

for i, score in enumerate(scores, start=1):
    print(f"Fold {i}: {score * 100:.2f}%")

print("\nAverage Accuracy:", round(scores.mean() * 100, 2), "%")
print("Standard Deviation:", round(scores.std() * 100, 2), "%")