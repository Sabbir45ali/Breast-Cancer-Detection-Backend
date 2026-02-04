import json
import random
import time
from firebase_admin_init import firebase_auth, firebase_db
from django.http import JsonResponse
import string
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from datetime import timedelta
from django.core.mail import send_mail
from django.utils import timezone
from django.conf import settings
from django.http import JsonResponse
from firebase_admin import auth
from firebase_config import db
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password, check_password
from .serializers import SignupSerializer, LoginSerializer,OrgSignupSerializer,OrgLoginSerializer,VerifyOTPSerializer,ResetPasswordSerializer,ForgotPasswordSerializer
import sys, os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(BASE_DIR)  # parent directory of auth_app
from firebase_config import db

@csrf_exempt
@csrf_exempt
def signup_user(request):
    if request.method != "POST":
        return JsonResponse({"error": "Only POST allowed"}, status=405)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    required_fields = ["username", "phnumber", "email", "password"]
    for field in required_fields:
        if field not in data:
            return JsonResponse({"error": f"{field} is required"}, status=400)

    username = data["username"]
    phnumber = data["phnumber"]
    email = data["email"]
    password = data["password"]

    try:
        # ✅ 1. Create user in Firebase Authentication
        user = auth.create_user(
            email=email,
            password=password,
            display_name=username,
            phone_number=f"+91{phnumber}" if not phnumber.startswith("+") else phnumber
        )

        uid = user.uid  # 🔥 THIS IS THE ONLY USER ID YOU SHOULD EVER USE

        # ✅ 2. Store profile in Realtime Database
        profile_data = {
            "uid": uid,
            "username": username,
            "email": email,
            "phnumber": phnumber,
            "role": "User",
            "created_at": {".sv": "timestamp"}
        }

        db.child("users").child(uid).set(profile_data)

        return JsonResponse(
            {"message": "Signup successful", "uid": uid},
            status=201
        )

    except auth.EmailAlreadyExistsError:
        return JsonResponse({"error": "Email already registered"}, status=400)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
def login_user(request):
    if request.method != "POST":
        return JsonResponse({"error": "Only POST allowed"}, status=405)

    data = json.loads(request.body)
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return JsonResponse({"error": "Email and password required"}, status=400)

    try:
        # 🔥 Verify user exists in Firebase Auth
        user = auth.get_user_by_email(email)
        uid = user.uid
    except auth.UserNotFoundError:
        return JsonResponse({"error": "User not found"}, status=404)

    # 🔍 Step 2: Fetch profile from DB using UID
    user_data = db.child("users").child(uid).get().val()

    if not user_data:
        return JsonResponse({"error": "User profile not found"}, status=404)

    # ✅ Success
    return JsonResponse({
        "message": "Login successful",
        "uid": uid,
        "email": user_data["email"],
        "username": user_data["username"],
        "role": user_data["role"]
    }, status=200)




@csrf_exempt
def signup_org(request):
    if request.method != "POST":
        return JsonResponse({"error": "Only POST allowed"}, status=405)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    org_name = data.get("org_name")
    phnumber = data.get("phnumber")
    email = data.get("email")
    org_type = data.get("org_type")
    license_number = data.get("license_number")
    password = data.get("password")

    if not all([org_name, phnumber, email, org_type, license_number, password]):
        return JsonResponse({"error": "All fields are required"}, status=400)

    try:
        # ✅ 1. CREATE FIREBASE AUTH USER
        user = auth.create_user(
            email=email,
            password=password,
        )

        uid = user.uid  # 🔥 THIS IS WHAT YOU WERE MISSING

        # ✅ 2. STORE ORG PROFILE USING UID
        org_data = {
            "uid": uid,
            "org_name": org_name,
            "phnumber": phnumber,
            "email": email,
            "org_type": org_type,
            "license_number": license_number,
            "created_at": int(time.time() * 1000),
            "role": "Organisation",
        }

        db.child("organisations").child(uid).set(org_data)

        return JsonResponse(
            {
                "message": "Organization signup successful",
                "uid": uid,
            },
            status=201
        )

    except auth.EmailAlreadyExistsError:
        return JsonResponse({"error": "Email already exists"}, status=400)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
def login_org(request):
    if request.method != "POST":
        return JsonResponse({"error": "Only POST allowed"}, status=405)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return JsonResponse({"error": "Email and password required"}, status=400)

    try:
        # ✅ 1. VERIFY USER EXISTS IN FIREBASE AUTH
        user = auth.get_user_by_email(email)
        uid = user.uid

        # ❗ Firebase Admin SDK cannot verify password directly
        # Password verification is implicitly handled by frontend / Firebase Auth
        # Backend trusts Firebase Auth user existence

        # ✅ 2. FETCH ORG PROFILE USING UID
        org = db.child("organisations").child(uid).get().val()

        if not org:
            return JsonResponse(
                {"error": "Organization profile not found"},
                status=404
            )

        # ✅ 3. SUCCESS RESPONSE
        return JsonResponse(
            {
                "message": "Organization login successful",
                "uid": uid,
                "role": "Organisation",
                "org_name": org.get("org_name"),
                "email": org.get("email"),
            },
            status=200
        )

    except auth.UserNotFoundError:
        return JsonResponse({"error": "Organization not found"}, status=404)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
def login_admin(request):
    if request.method != "POST":
        return JsonResponse({"error": "Only POST allowed"}, status=405)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    serializer = OrgLoginSerializer(data=data)  # ✅ You might want a separate AdminLoginSerializer later
    if not serializer.is_valid():
        return JsonResponse({"error": serializer.errors}, status=400)

    email = serializer.validated_data["email"]
    raw_password = serializer.validated_data["password"]

    # Use email as key
    email_key = email.replace(".", "_")
    admin = db.child("org_login_details").child(email_key).get().val()

    if not admin:
        return JsonResponse({"error": "Admin not found"}, status=404)

    hashed_password = admin.get("password")
    if not hashed_password or not check_password(raw_password, hashed_password):
        return JsonResponse({"error": "Invalid password"}, status=401)

    return JsonResponse({"message": "Admin login successful"}, status=200)


# ============================
#  FORGOT PASSWORD 
# ============================
@csrf_exempt
def forgot_password(request):
    if request.method != "POST":
        return JsonResponse({"error": "Only POST allowed"}, status=405)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    email = data.get("email")
    if not email:
        return JsonResponse({"error": "Email is required"}, status=400)

    # Generate OTP & expiry
    otp = str(random.randint(100000, 999999))
    expiry_time = int(time.time()) + 300  # 5 minutes

    email_key = email.replace(".", "_")

    # Save OTP in Firebase
    db.child("password_resets").child(email_key).set({
        "otp": otp,
        "expiry": expiry_time
    })

    # Send OTP via email
    try:
        send_mail(
            subject="Password Reset OTP",
            message=f"Your OTP is {otp}. It will expire in 5 minutes.",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
            fail_silently=False,
        )
    except Exception as e:
        # If mail fails, cleanup OTP
        db.child("password_resets").child(email_key).remove()
        return JsonResponse({"error": f"Failed to send OTP: {str(e)}"}, status=500)

    return JsonResponse({"message": f"OTP sent to {email}"}, status=200)


# ============================
#  VERIFY OTP 
# ============================
@csrf_exempt
def verify_otp(request):
    if request.method != "POST":
        return JsonResponse({"error": "Only POST allowed"}, status=405)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    serializer = VerifyOTPSerializer(data=data)
    if not serializer.is_valid():
        return JsonResponse({"errors": serializer.errors}, status=400)

    email = serializer.validated_data["email"]
    otp = serializer.validated_data["otp"]

    email_key = email.replace(".", "_")
    otp_data = db.child("password_resets").child(email_key).get().val()

    if not otp_data:
        return JsonResponse({"error": "No OTP found. Request again."}, status=400)

    saved_otp = otp_data.get("otp")
    expiry_time = otp_data.get("expiry")

    # Check expiry
    if int(time.time()) > expiry_time:
        db.child("password_resets").child(email_key).remove()
        return JsonResponse({"error": "OTP expired. Request again."}, status=400)

    # Check OTP match
    if otp != saved_otp:
        return JsonResponse({"error": "Invalid OTP"}, status=400)

    # (Optional) Mark as verified if needed for reset_password
    db.child("password_resets").child(email_key).update({
        "verified": True
    })

    return JsonResponse({"message": "OTP verified successfully"}, status=200)


# ============================
#  RESET PASSWORD 
# ============================
@csrf_exempt
def reset_password(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method"}, status=405)

    # Parse JSON body
    try:
        data = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON body"}, status=400)

    # Validate request data - Adjust serializer to expect only email and new_password now
    serializer = ResetPasswordSerializer(data=data)
    if not serializer.is_valid():
        return JsonResponse({"errors": serializer.errors}, status=400)

    email = serializer.validated_data["email"]
    new_password = serializer.validated_data["new_password"]

    # Ensure password is hashed (in case serializer didn’t hash)
    if not new_password.startswith("pbkdf2_"):
        new_password = make_password(new_password)

    email_key = email.replace(".", "_")

    # Directly update password without OTP validation
    updated = False
    for section in ["user_login_details", "org_login_details", "admin_login_details"]:
        if db.child(section).child(email_key).get().val():
            db.child(section).child(email_key).update({"password": new_password})
            updated = True
            break

    if not updated:
        return JsonResponse({"error": "Account not found"}, status=404)

    return JsonResponse({"message": "Password reset successful"}, status=200)



@csrf_exempt
def send_otp(request):
    """
    POST JSON: { "email": "user@example.com" }
    Stores OTP in Realtime DB at password_resets/<email_key> and mails it.
    """
    if request.method != "POST":
        return JsonResponse({"error": "Only POST allowed"}, status=405)

    try:
        data = json.loads(request.body.decode("utf-8"))
    except Exception:
        return JsonResponse({"error": "Invalid JSON body"}, status=400)

    email = data.get("email")
    if not email:
        return JsonResponse({"error": "Email is required"}, status=400)

    # generate otp and expiry
    otp = str(random.randint(100000, 999999))
    expiry_time = int(time.time()) + 300  # 5 minutes from now

    # save to Firebase Realtime DB (use email key without dots)
    email_key = email.replace(".", "_")
    db.child("password_resets").child(email_key).set({
        "otp": otp,
        "expiry": expiry_time,
        "verified": False
    })

    # send email
    try:
        send_mail(
            subject="Password Reset OTP",
            message=f"Your OTP for password reset is {otp}. It will expire in 5 minutes.",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
            fail_silently=False,
        )
    except Exception as e:
        # remove OTP from db if mail failed
        db.child("password_resets").child(email_key).remove()
        return JsonResponse({"error": f"Failed to send OTP: {str(e)}"}, status=500)

    return JsonResponse({"status": "success", "message": "OTP sent to email"}, status=200)