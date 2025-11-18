#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Heart Disease Prediction - Web Service
Flask API for heart disease prediction
"""

import pickle
import numpy as np
from flask import Flask, request, jsonify

# Configuration
MODEL_FILE = 'heart_disease_model.pkl'
THRESHOLD = 0.5

# Load model and preprocessing objects
print("Loading model...")
with open(MODEL_FILE, 'rb') as f:
    dv, scaler, model, categorical, numerical = pickle.load(f)
print("✓ Model loaded successfully!")

# Initialize Flask app
app = Flask('heart_disease_prediction')

@app.route('/predict', methods=['POST'])
def predict():
    """
    Predict heart disease probability
    
    Expected JSON input:
    {
        "Age": 52,
        "Sex": "M",
        "ChestPainType": "ASY",
        "RestingBP": 120,
        "Cholesterol": 280,
        "FastingBS": 0,
        "RestingECG": "Normal",
        "MaxHR": 150,
        "ExerciseAngina": "N",
        "Oldpeak": 2.5,
        "ST_Slope": "Flat"
    }
    """
    try:
        # Get patient data from request
        patient = request.get_json()
        
        # Validate required fields
        required_fields = ['Age', 'Sex', 'ChestPainType', 'RestingBP', 'Cholesterol', 
                          'FastingBS', 'RestingECG', 'MaxHR', 'ExerciseAngina', 
                          'Oldpeak', 'ST_Slope']
        
        missing_fields = [field for field in required_fields if field not in patient]
        if missing_fields:
            return jsonify({
                'error': f'Missing required fields: {missing_fields}'
            }), 400
        
        # Preprocess input
        # Encode binary variables
        patient_processed = patient.copy()
        patient_processed['Sex'] = 0 if patient['Sex'] == 'M' else 1
        patient_processed['ExerciseAngina'] = 0 if patient['ExerciseAngina'] == 'N' else 1
        
        # Extract numerical features
        X_num = np.array([[patient_processed[col] for col in numerical]])
        X_num_scaled = scaler.transform(X_num)
        
        # Extract and encode categorical features
        cat_dict = {col: patient_processed[col] for col in categorical}
        X_cat = dv.transform([cat_dict])
        
        # Combine features
        X = np.column_stack([X_num_scaled, X_cat])
        
        # Make prediction
        probability = float(model.predict_proba(X)[0, 1])
        prediction = int(probability >= THRESHOLD)
        
        # Prepare response
        result = {
            'heart_disease_probability': round(probability, 4),
            'heart_disease': bool(prediction),
            'risk_level': get_risk_level(probability),
            'message': get_message(probability)
        }
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'model': 'heart_disease_prediction',
        'version': '1.0'
    })

def get_risk_level(probability):
    """Determine risk level based on probability"""
    if probability < 0.3:
        return 'Low'
    elif probability < 0.6:
        return 'Medium'
    else:
        return 'High'

def get_message(probability):
    """Get recommendation message based on probability"""
    if probability < 0.3:
        return 'Low risk of heart disease. Maintain healthy lifestyle.'
    elif probability < 0.6:
        return 'Medium risk of heart disease. Consider medical consultation.'
    else:
        return 'High risk of heart disease. Seek immediate medical attention.'

if __name__ == '__main__':
    # Run the Flask app
    print("\n" + "="*60)
    print("Heart Disease Prediction Service")
    print("="*60)
    print("\nStarting server on http://0.0.0.0:9696")
    print("API Endpoints:")
    print("  POST /predict - Make predictions")
    print("  GET  /health  - Health check")
    print("\n" + "="*60 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=9696)
