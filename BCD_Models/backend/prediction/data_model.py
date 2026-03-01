import joblib
import os
import numpy as np
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "models_ml", "breast_model.pkl")
SCALER_PATH = os.path.join(BASE_DIR, "models_ml", "scaler.pkl")
# Load model and scaler once
model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)
def predict_data(input_data):
    # Convert dictionary to ordered list
    values = list(input_data.values())
    values = np.array(values).reshape(1, -1)
    # Apply scaling
    scaled_values = scaler.transform(values)
    # Predict
    prediction = model.predict(scaled_values)[0]
    probability = model.predict_proba(scaled_values)[0][1]
    if prediction == 1:
        result = "Malignant"
    else:
        result = "Benign"
    return result, round(probability, 3)