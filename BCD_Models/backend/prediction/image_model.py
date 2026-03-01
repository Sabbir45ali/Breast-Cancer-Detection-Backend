import tensorflow as tf
import numpy as np
import os
from PIL import Image
###################################
# LOAD CNN MODEL
###################################
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "models_ml", "imageClassification.keras")
model = tf.keras.models.load_model(MODEL_PATH)
###################################
# IMAGE PREDICTION FUNCTION
###################################
def predict_image(image_file):
    # Open image
    img = Image.open(image_file)
    # Convert to RGB
    img = img.convert("RGB")
   # Resize to model input size
    img = img.resize((224,224))
    # Convert to array
    img = np.array(img)
    # Normalize
    img = img / 255.0
    # Add batch dimension
    img = np.expand_dims(img, axis=0)
    ###################################
    # PREDICT
    ###################################
    prediction = model.predict(img)[0][0]
    ###################################
    # RESULT
    ###################################
    if prediction > 0.5:
        result = "Malignant"
        confidence = float(prediction)
    else:
        result = "Benign"
        confidence = float(1 - prediction)
    return result, round(confidence,3)