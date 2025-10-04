import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix

# Read and sort data
data = pd.read_csv("../results/merged_fin_tec.csv")
print("Start data preprocessing")
data = data.sort_values(by=['Year', 'Month']).reset_index(drop=True)

# Handle missing values
data = data.ffill()

# Calculate month-over-month differences (fundamentals)
data['Asset_Diff'] = data['Total_Assets'].diff()
data['Liability_Diff'] = data['Total_Liabilities'].diff()
data['Equity_Diff'] = data['Total_Equity'].diff()

# Shift all features by 1 month
# ensures we only use info from month (t−1) to predict movement at month (t)
shift_cols = ['Asset_Diff', 'Liability_Diff', 'Equity_Diff']
data[shift_cols] = data[shift_cols].shift(1)

# Create target: price movement (1 if next month up, else 0)
# (Close at t) > (Close at t−1)
data['y'] = (data['Close'].diff() > 0).astype(int) # pyright: ignore[reportOperatorIssue]

# Drop NaN rows caused by diff & shift
data = data.dropna().reset_index(drop=True)

# Save preprocessed data
data.to_csv("../results/final_data.csv", index=False, encoding="utf-8-sig")
print("Final data saved")
print(data.head())

# Feature selection
features = ['Asset_Diff', 'Liability_Diff', 'Equity_Diff']
target = 'y'
print("Features selected:", features)

X = data[features]
y = data[target]

# Normalize features (Z-score)
X = (X - X.mean()) / X.std()
print(X.head())

# Time-based train-test split
train_mask = (data['Year'] < 2024)
test_mask = (data['Year'] == 2024)

X_train, X_test = X[train_mask], X[test_mask]
y_train, y_test = y[train_mask], y[test_mask]
print(f"Train size: {len(X_train)}, Test size: {len(X_test)}")

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate model
y_pred = model.predict(X_test)
print(confusion_matrix(y_test, y_pred))
print(classification_report(y_test, y_pred))

# Feature importance
importances = model.feature_importances_
feature_names = X.columns
feature_importance_df = pd.DataFrame({'Feature': feature_names, 'Importance': importances})
print(feature_importance_df.sort_values(by='Importance', ascending=False))

# Accuracy (R² score for classification)
r2_score = model.score(X_test, y_test)
print(f"R2 Score (Accuracy): {r2_score:.3f}")