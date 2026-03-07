from fastapi import FastAPI, UploadFile, File, Request, HTTPException
import joblib
import os
import numpy as np
import tensorflow as tf
from PIL import Image
import io

app = FastAPI(title="Breast Cancer Detection ML API")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# -----------------
# Load Models
# -----------------
try:
    # Tabular Data Models
    MODEL_PATH = os.path.join(BASE_DIR, "models_ml", "breast_model.pkl")
    SCALER_PATH = os.path.join(BASE_DIR, "models_ml", "scaler.pkl")
    tabular_model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)

    # Image Model
    IMAGE_MODEL_PATH = os.path.join(BASE_DIR, "models_ml", "imageClassification.keras")
    image_model = tf.keras.models.load_model(IMAGE_MODEL_PATH)
except Exception as e:
    print(f"Error loading models: {e}")


@app.get("/")
def read_root():
    return {"status": "ML API is running."}


@app.post("/predict/data")
async def predict_data_api(request: Request):
    try:
        input_data = await request.json()
        if not input_data:
            raise HTTPException(status_code=400, detail="No input data provided")

        values = list(input_data.values())
        values_array = np.array(values).reshape(1, -1)
        
        # Apply scaling
        scaled_values = scaler.transform(values_array)
        
        # Predict
        prediction = tabular_model.predict(scaled_values)[0]
        probability = tabular_model.predict_proba(scaled_values)[0][1]
        
        result = "Malignant" if prediction == 1 else "Benign"
        
        return {
            "result": result,
            "probability": round(float(probability), 3) # ensure it's JSON serializable
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/predict/image")
async def predict_image_api(image: UploadFile = File(...)):
    try:
        # Read image
        contents = await image.read()
        img = Image.open(io.BytesIO(contents))
        img = img.convert("RGB")
        img = img.resize((224, 224))
        
        # Preprocessing
        img_array = np.array(img)
        img_array = img_array / 255.0
        img_array = np.expand_dims(img_array, axis=0)

        # Predict
        prediction = image_model.predict(img_array)[0][0]

        if prediction > 0.5:
            result = "Malignant"
            confidence = float(prediction)
        else:
            result = "Benign"
            confidence = float(1 - prediction)

        return {
            "result": result,
            "confidence": round(confidence, 3)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
