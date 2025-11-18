#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Heart Disease Prediction - Training Script
This script trains the final model and saves it to a pickle file.
"""

import pandas as pd
import numpy as np
import pickle
import warnings
warnings.filterwarnings('ignore')

from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.feature_extraction import DictVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score, classification_report

# Configuration
DATA_FILE = 'heart.csv'
OUTPUT_MODEL = 'heart_disease_model.pkl'
RANDOM_STATE = 1
TEST_SIZE = 0.2
VAL_SIZE = 0.25  # 25% of remaining data after test split

print("="*60)
print("Heart Disease Prediction - Model Training")
print("="*60)

# 1. Load and prepare data
print("\n[1/5] Loading data...")
df = pd.read_csv(DATA_FILE)
print(f"✓ Loaded {df.shape[0]} records with {df.shape[1]} features")

# 2. Data preprocessing
print("\n[2/5] Preprocessing data...")

# Encode binary categorical variables
df['Sex'] = df['Sex'].map({'M': 0, 'F': 1})
df['ExerciseAngina'] = df['ExerciseAngina'].map({'N': 0, 'Y': 1})

# Identify feature types
categorical = df.select_dtypes(include=['object']).columns.tolist()
numerical = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
numerical.remove('HeartDisease')

print(f"✓ Categorical features: {categorical}")
print(f"✓ Numerical features: {numerical}")

# Split features and target
X = df.drop('HeartDisease', axis=1)
y = df['HeartDisease']

# 3. Train-Val-Test split
print("\n[3/5] Splitting data...")
df_full_train, X_test, y_full_train, y_test = train_test_split(
    X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=y
)

X_train, X_val, y_train, y_val = train_test_split(
    df_full_train, y_full_train, test_size=VAL_SIZE, 
    random_state=RANDOM_STATE, stratify=y_full_train
)

print(f"✓ Training set: {X_train.shape[0]} samples")
print(f"✓ Validation set: {X_val.shape[0]} samples")
print(f"✓ Test set: {X_test.shape[0]} samples")

# 4. Feature encoding and scaling
print("\n[4/5] Encoding and scaling features...")

# One-hot encoding for categorical features
dv = DictVectorizer(sparse=False)
train_dict = X_train[categorical].to_dict(orient='records')
X_train_cat = dv.fit_transform(train_dict)

val_dict = X_val[categorical].to_dict(orient='records')
X_val_cat = dv.transform(val_dict)

test_dict = X_test[categorical].to_dict(orient='records')
X_test_cat = dv.transform(test_dict)

# Standardize numerical features
scaler = StandardScaler()
X_train_num = scaler.fit_transform(X_train[numerical].values)
X_val_num = scaler.transform(X_val[numerical].values)
X_test_num = scaler.transform(X_test[numerical].values)

# Combine features
X_train_processed = np.column_stack([X_train_num, X_train_cat])
X_val_processed = np.column_stack([X_val_num, X_val_cat])
X_test_processed = np.column_stack([X_test_num, X_test_cat])

print(f"✓ Final feature shape: {X_train_processed.shape}")

# 5. Model training with hyperparameter tuning
print("\n[5/5] Training model with hyperparameter tuning...")
print("This may take a few minutes...")

param_grid = {
    'n_estimators': [100, 200, 300],
    'max_depth': [10, 15, 20, None],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4]
}

grid_search = GridSearchCV(
    RandomForestClassifier(random_state=RANDOM_STATE, n_jobs=-1),
    param_grid=param_grid,
    cv=5,
    scoring='roc_auc',
    verbose=1,
    n_jobs=-1
)

grid_search.fit(X_train_processed, y_train)

best_model = grid_search.best_estimator_

print(f"\n✓ Best parameters: {grid_search.best_params_}")
print(f"✓ Best cross-validation ROC-AUC: {grid_search.best_score_:.4f}")

# Validation performance
y_pred_val = best_model.predict_proba(X_val_processed)[:, 1]
y_pred_val_class = (y_pred_val >= 0.5).astype(int)

val_acc = accuracy_score(y_val, y_pred_val_class)
val_f1 = f1_score(y_val, y_pred_val_class)
val_auc = roc_auc_score(y_val, y_pred_val)

print(f"\nValidation Results:")
print(f"  Accuracy: {val_acc:.4f}")
print(f"  F1-Score: {val_f1:.4f}")
print(f"  ROC-AUC: {val_auc:.4f}")

# Test performance
y_pred_test = best_model.predict_proba(X_test_processed)[:, 1]
y_pred_test_class = (y_pred_test >= 0.5).astype(int)

test_acc = accuracy_score(y_test, y_pred_test_class)
test_f1 = f1_score(y_test, y_pred_test_class)
test_auc = roc_auc_score(y_test, y_pred_test)

print(f"\nTest Results:")
print(f"  Accuracy: {test_acc:.4f}")
print(f"  F1-Score: {test_f1:.4f}")
print(f"  ROC-AUC: {test_auc:.4f}")

print(f"\nClassification Report (Test Set):")
print(classification_report(y_test, y_pred_test_class))

# 6. Save model
print(f"\n[6/6] Saving model to '{OUTPUT_MODEL}'...")
with open(OUTPUT_MODEL, 'wb') as f:
    pickle.dump((dv, scaler, best_model, categorical, numerical), f)

print(f"✓ Model saved successfully!")
print("\n" + "="*60)
print("Training completed successfully!")
print("="*60)
