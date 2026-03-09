from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response
from rest_framework import status

from backend.authentication import FirebaseAuthentication

from firebase_config import db
import requests

from datetime import datetime
import cloudinary
import cloudinary.uploader
import os
import uuid

from firebase_admin import firestore

ML_SERVICE_URL = os.getenv("ML_SERVICE_URL", "http://127.0.0.1:8000")

cloudinary.config(
cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
api_key=os.getenv("CLOUDINARY_API_KEY"),
api_secret=os.getenv("CLOUDINARY_API_SECRET")
)
###################################
# ORG DATA PREDICTION API
###################################
@api_view(['POST']) 
@authentication_classes([FirebaseAuthentication])
def org_predict_data(request):
    uid = request.user
    # Check organization
    org_doc = db.collection("organizations").document(uid).get()
    if not org_doc.exists:
        return Response({
            "error": "Only organizations allowed"
        }, status=status.HTTP_403_FORBIDDEN)
    try:
        input_data = request.data
        
        # PROXY: Forward request to ML API
        response = requests.post(f"{ML_SERVICE_URL}/predict/data", json=input_data)
        if response.status_code != 200:
            return Response({"error": "Failed to get prediction from ML API"}, status=status.HTTP_502_BAD_GATEWAY)
            
        ml_data = response.json()
        result = ml_data.get("result")
        probability = ml_data.get("probability")
        org_data = org_doc.to_dict()
        ###################################
        # SAVE TO FIREBASE
        ###################################
        db.collection("prediction_results").add({
            "uid": uid,
            "org_name": org_data["org_name"],
            "input": input_data,
            "result": result,
            "probability": probability,
            "timestamp": datetime.now()
        })
        ###################################
        return Response({
            "result": result,
            "probability": probability
        })
    except Exception as e:
        return Response({
            "error": str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
###################################
# ORG PREDICTION HISTORY API
###################################
@api_view(['GET'])
@authentication_classes([FirebaseAuthentication])
def org_history(request):
    uid = request.user
    # Check organization
    org_doc = db.collection("organizations").document(uid).get()
    if not org_doc.exists:
        return Response({
            "error": "Only organizations allowed"
        })
    ###################################
    # GET HISTORY FROM FIRESTORE
    ###################################
    docs = db.collection("prediction_results") \
             .where("uid", "==", uid) \
             .stream()
    history = []
    for doc in docs:
        data = doc.to_dict()
        history.append({
            "result": data["result"],
            "probability": data["probability"],
            "input": data["input"],
            "timestamp": data["timestamp"]
        })
    return Response(history)

@api_view(['POST'])
@authentication_classes([FirebaseAuthentication])
def predict_image_api(request):
    uid = request.user
    image = request.FILES.get('image')
    if not image:
        return Response({
            "error":"No image uploaded"
        }, status=status.HTTP_400_BAD_REQUEST)
    ###################################
    # PREDICT VIA ML MICROSERVICE
    ###################################
    try:
        image.seek(0)
        files = {"image": (image.name, image.read(), image.content_type)}
        response = requests.post(f"{ML_SERVICE_URL}/predict/image", files=files)
        
        if response.status_code != 200:
            return Response({"error": f"Failed prediction: {response.text}"}, status=status.HTTP_502_BAD_GATEWAY)
            
        ml_data = response.json()
        result = ml_data.get("result")
        confidence = ml_data.get("confidence")
    except Exception as e:
        return Response({"error": f"ML service error: {str(e)}"}, status=status.HTTP_502_BAD_GATEWAY)

    ###################################
    # UPLOAD TO CLOUDINARY
    ###################################
    try:
        image.seek(0)
        upload_result = cloudinary.uploader.upload(
            image,
            folder="breast_cancer_images"
        )
        image_url = upload_result['secure_url']
    except Exception as e:
        return Response({
            "result": result,
            "confidence": confidence,
            "image_url": None,
            "warning": f"Prediction succeeded but image upload failed: {str(e)}"
        })

    ###################################
    # DETECT ROLE
    ###################################
    role="user"
    if db.collection("organizations").document(uid).get().exists:
        role="org"
    ###################################
    # SAVE TO FIRESTORE
    ###################################
    try:
        db.collection("image_results").add({
            "uid":uid,
            "role":role,
            "image_url":image_url,
            "image_name": image.name,
            "result":result,
            "confidence":confidence,
            "timestamp":datetime.now()
        })
    except Exception as e:
        return Response({
            "result": result,
            "confidence": confidence,
            "image_url": image_url,
            "warning": f"Prediction succeeded but history save failed: {str(e)}"
        })
    ###################################
    return Response({
        "result":result,
        "confidence":confidence,
        "image_url":image_url
    })

###################################
# IMAGE HISTORY API
###################################
@api_view(['GET'])
@authentication_classes([FirebaseAuthentication])
def image_history(request):
    uid = request.user
    ###################################
    # FETCH FROM FIRESTORE
    ###################################
    docs = db.collection("image_results") \
             .where("uid","==",uid) \
             .stream()
    history = []
    for doc in docs:
        data = doc.to_dict()
        history.append({
            "image_url": data["image_url"],
            "result": data["result"],
            "confidence": data["confidence"],
            "timestamp": data["timestamp"]
        })
    return Response(history)

@api_view(['GET'])
@authentication_classes([FirebaseAuthentication])
def org_full_history(request):

    uid = request.user

    db = firestore.client()

    history = []


    ############################
    # DATA HISTORY
    ############################

    data_docs = db.collection('prediction_results') \
        .where('uid', '==', uid).stream()

    for doc in data_docs:

        d = doc.to_dict()

        timestamp = d.get("timestamp")

        # Convert timestamp safely
        if timestamp:
            try:
                date = timestamp.isoformat()
            except:
                date = str(timestamp)
        else:
            date = ""

        history.append({

            "type": "data",

            "date": date,

            "result": d.get("result"),

            "inputs": d.get("input")

        })


    ############################
    # IMAGE HISTORY
    ############################

    img_docs = db.collection('image_results') \
        .where('uid', '==', uid).stream()

    for doc in img_docs:

        d = doc.to_dict()

        timestamp = d.get("timestamp")

        # Convert timestamp safely
        if timestamp:
            try:
                date = timestamp.isoformat()
            except:
                date = str(timestamp)
        else:
            date = ""

        image_url = d.get("image_url", "")

        # Extract image name from url
        image_name = ""

        if image_url:
            import os
            image_name = os.path.basename(image_url)

        history.append({

            "type": "image",

            "date": date,

            "result": d.get("result"),

            "image_name": image_name,

            "image_url": image_url   # ✅ Added image link

        })


    ############################
    # SORT BY DATE
    ############################

    history.sort(
        key=lambda x: x["date"] if x["date"] else "",
        reverse=True
    )


    return Response(history)

###################################
# DEBUG: Test ML Service Connection
###################################
@api_view(['GET'])
def debug_ml_service(request):
    """Debug endpoint to check ML_SERVICE_URL connectivity"""
    ml_url = os.getenv("ML_SERVICE_URL", "NOT SET")
    try:
        response = requests.get(f"{ML_SERVICE_URL}/", timeout=10)
        return Response({
            "ml_service_url": ml_url,
            "ml_service_status": response.status_code,
            "ml_service_response": response.json()
        })
    except Exception as e:
        return Response({
            "ml_service_url": ml_url,
            "ml_service_error": str(e)
        }, status=status.HTTP_502_BAD_GATEWAY)