#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test script for Heart Disease Prediction API
"""

import requests

# API endpoint
url = 'http://localhost:9696/predict'

# Test case 1: High risk patient
patient_high_risk = {
    "Age": 65,
    "Sex": "M",
    "ChestPainType": "ASY",
    "RestingBP": 160,
    "Cholesterol": 350,
    "FastingBS": 1,
    "RestingECG": "ST",
    "MaxHR": 110,
    "ExerciseAngina": "Y",
    "Oldpeak": 3.5,
    "ST_Slope": "Flat"
}

# Test case 2: Low risk patient
patient_low_risk = {
    "Age": 35,
    "Sex": "F",
    "ChestPainType": "ATA",
    "RestingBP": 110,
    "Cholesterol": 180,
    "FastingBS": 0,
    "RestingECG": "Normal",
    "MaxHR": 170,
    "ExerciseAngina": "N",
    "Oldpeak": 0.0,
    "ST_Slope": "Up"
}

print("="*60)
print("Testing Heart Disease Prediction API")
print("="*60)

# Test health endpoint
print("\n[1] Testing health endpoint...")
try:
    response = requests.get('http://localhost:9696/health')
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
except Exception as e:
    print(f"Error: {e}")

# Test prediction for high risk patient
print("\n[2] Testing prediction for HIGH RISK patient...")
print(f"Input: {patient_high_risk}")
try:
    response = requests.post(url, json=patient_high_risk)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
except Exception as e:
    print(f"Error: {e}")

# Test prediction for low risk patient
print("\n[3] Testing prediction for LOW RISK patient...")
print(f"Input: {patient_low_risk}")
try:
    response = requests.post(url, json=patient_low_risk)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
except Exception as e:
    print(f"Error: {e}")

print("\n" + "="*60)
print("Testing completed!")
print("="*60)
