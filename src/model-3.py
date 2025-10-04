import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix

# Load and sort data
data = pd.read_csv("../results/merged_fin_tec.csv")
print("Start data preprocessing")
data = data.sort_values(by=['Year', 'Month']).reset_index(drop=True)

# Fill missing financial values with last known value
data = data.ffill()

# Calculate month-over-month differences (fundamental features)
data['Asset_Diff'] = data['Total_Assets'].diff()
data['Liability_Diff'] = data['Total_Liabilities'].diff()
data['Equity_Diff'] = data['Total_Equity'].diff()

# Technical indicators
data['Close_Diff'] = data['Close'].diff()

# 3-month moving average
data['MA3'] = data['Close'].rolling(window=3).mean()

# RSI function
def compute_rsi(series, window=3):
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

data['RSI'] = compute_rsi(data['Close'], window=3)

# Shift all feature columns by 1 month
# This ensures we only use information available *before* the target month
shift_cols = ['Asset_Diff', 'Liability_Diff', 'Equity_Diff', 'Close_Diff', 'MA3', 'RSI']
data[shift_cols] = data[shift_cols].shift(1)

#Create target: price movement next month
data['y'] = (data['Close'].shift(-1) > data['Close']).astype(int)

# Clean NaN rows caused by diff, rolling, shift, etc.
data = data.dropna().reset_index(drop=True)

# Save preprocessed data
data.to_csv("../results/final_data.csv", index=False, encoding="utf-8-sig")
print("Final data saved")
print(data.head())

# Select features and target
features = ['Asset_Diff', 'Liability_Diff', 'Equity_Diff', 'Close_Diff', 'MA3', 'RSI']
target = 'y'
print("Features selected:", features)

X = data[features]
y = data[target]

# Normalize features (z-score)
X = (X - X.mean()) / X.std()
print(X.head())

# Split data by time
train_mask = (data['Year'] < 2024)
test_mask = (data['Year'] == 2024)

X_train, X_test = X[train_mask], X[test_mask]
y_train, y_test = y[train_mask], y[test_mask]
print(f"Train size: {len(X_train)}, Test size: {len(X_test)}")

# Train Random Forest model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
print(confusion_matrix(y_test, y_pred))
print(classification_report(y_test, y_pred))

# Feature importance
importances = model.feature_importances_
feature_names = X.columns
feature_importance_df = pd.DataFrame({'Feature': feature_names, 'Importance': importances})
print(feature_importance_df.sort_values(by="Importance", ascending=False))

# Accuracy on test
r2_score = model.score(X_test, y_test)
print(f"R2 Score (Accuracy): {r2_score:.3f}")