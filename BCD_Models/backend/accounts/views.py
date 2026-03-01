import requests
import os
from rest_framework.decorators import api_view
from rest_framework.response import Response
from firebase_admin import auth
from firebase_config import db
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response
from backend.authentication import FirebaseAuthentication
###################################
# USER SIGNUP
###################################
@api_view(['POST'])
def user_signup(request):
    name = request.data.get('name')
    phone = request.data.get('phone')
    email = request.data.get('email')
    password = request.data.get('password')
    try:
        user = auth.create_user(
            email=email,
            password=password
        )
        uid = user.uid
        db.collection("users").document(uid).set({
            "uid":uid,
            "role":"user",
            "name":name,
            "phone":phone,
            "email":email
        })
        return Response({
            "message":"User Signup Successful",
            "uid":uid
        })
    except Exception as e:
        return Response({
            "error":str(e)
        })
        
###################################
# ORGANIZATION SIGNUP
###################################
@api_view(['POST'])
def org_signup(request):
    org_name = request.data.get('org_name')
    phone = request.data.get('phone')
    email = request.data.get('email')
    org_type = request.data.get('type')
    license = request.data.get('license')
    password = request.data.get('password')
    try:
        user = auth.create_user(
            email=email,
            password=password
        )
        uid = user.uid
        db.collection("organizations").document(uid).set({
            "uid":uid,
            "role":"org",
            "org_name":org_name,
            "phone":phone,
            "email":email,
            "type":org_type,
            "license":license
        })
        return Response({
            "message":"Organization Signup Successful",
            "uid":uid
        })
    except Exception as e:
        return Response({
            "error":str(e)
        })
        
###################################
# USER LOGIN
###################################
@api_view(['POST'])
def user_login(request):
    email = request.data.get('email')
    password = request.data.get('password')
    url = "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword"
    payload = {
        "email": email,
        "password": password,
        "returnSecureToken": True
    }
    params = {
        "key": os.getenv("FIREBASE_API_KEY")
    }
    res = requests.post(url, params=params, json=payload)
    data = res.json()
    if "idToken" not in data:
        return Response(data)
    uid = data["localId"]
    doc = db.collection("users").document(uid).get()
    user_data = doc.to_dict()
    return Response({
        "message":"Login Successful",
        "uid":uid,
        "role":"user",
        "name":user_data["name"],
        "token":data["idToken"]
    })

###################################
# ORG LOGIN
###################################

@api_view(['POST'])
def org_login(request):
    email = request.data.get('email')
    password = request.data.get('password')
    url = "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword"
    payload = {
        "email": email,
        "password": password,
        "returnSecureToken": True
    }
    params = {
        "key": os.getenv("FIREBASE_API_KEY")
    }
    res = requests.post(url, params=params, json=payload)
    data = res.json()
    if "idToken" not in data:
        return Response({
            "error":"Invalid email or password"
        })
    uid = data["localId"]
    doc = db.collection("organizations").document(uid).get()
    org_data = doc.to_dict()
    return Response({
        "message":"Org Login Successful",
        "uid":uid,
        "role":"org",
        "org_name":org_data["org_name"],
        "token":data["idToken"]
    })
###################################
# USER PROFILE API
###################################
@api_view(['GET'])
@authentication_classes([FirebaseAuthentication])
def user_profile(request):
    uid = request.user
    doc = db.collection("users").document(uid).get()
    if not doc.exists:
        return Response({
            "error":"User not found"
        })
    data = doc.to_dict()
    return Response({
        "name":data["name"],
        "email":data["email"],
        "phone":data["phone"],
        "age":data.get("age"),
        "blood_group":data.get("blood_group"),
        "height":data.get("height"),
        "weight":data.get("weight"),
        "medical_history":data.get("medical_history"),
        "symptoms":data.get("symptoms"),
        "role":"user"
    })
###################################
# ORG PROFILE API
###################################
@api_view(['GET'])
@authentication_classes([FirebaseAuthentication])
def org_profile(request):
    uid = request.user
    doc = db.collection("organizations").document(uid).get()
    if not doc.exists:
        return Response({
            "error":"Organization not found"
        })
    data = doc.to_dict()
    return Response({
        "org_name":data["org_name"],
        "email":data["email"],
        "phone":data["phone"],
        "type":data["type"],
        "license":data["license"],
        "role":"org"
    })

###################################
# UPDATE USER PROFILE
###################################
@api_view(['POST'])
@authentication_classes([FirebaseAuthentication])
def update_user_profile(request):
    uid = request.user
    age = request.data.get("age")
    blood = request.data.get("blood_group")
    height = request.data.get("height")
    weight = request.data.get("weight")
    history = request.data.get("medical_history")
    symptoms = request.data.get("symptoms")
    ###################################
    # UPDATE FIRESTORE
    ###################################
    db.collection("users").document(uid).update({
        "age":age,
        "blood_group":blood,
        "height":height,
        "weight":weight,
        "medical_history":history,
        "symptoms":symptoms
    })
    return Response({
        "message":"Profile Updated Successfully"
    })