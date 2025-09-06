import json
import random
import time
import string
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from datetime import timedelta
from django.core.mail import send_mail
from django.utils import timezone
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password, check_password
from .serializers import SignupSerializer, LoginSerializer,OrgSignupSerializer,OrgLoginSerializer,VerifyOTPSerializer,ResetPasswordSerializer,ForgotPasswordSerializer
import sys, os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(BASE_DIR)  # parent directory of auth_app
from firebase_config import db

@csrf_exempt
def signup_user(request):
    if request.method != "POST":
        return JsonResponse({"error": "Only POST allowed"}, status=405)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    serializer = SignupSerializer(data=data)
    if not serializer.is_valid():
        return JsonResponse({"error": serializer.errors}, status=400)

    username = serializer.validated_data["username"]
    phnumber = serializer.validated_data["phnumber"]
    email = serializer.validated_data["email"]
    raw_password = serializer.validated_data["password"]

    # ✅ Create Firebase-safe key
    email_key = email.replace(".", "_")

    # ✅ Check if this email already exists
    existing_user = db.child("user_login_details").child(email_key).get().val()
    if existing_user:
        return JsonResponse({"error": "Email already exists"}, status=400)

    # ✅ Check username/phone uniqueness (loop required)
    all_users = db.child("user_login_details").get().val() or {}
    for user in all_users.values():
        if user.get("username") == username:
            return JsonResponse({"error": "Username already exists"}, status=400)
        if user.get("phnumber") == phnumber:
            return JsonResponse({"error": "Phone number already exists"}, status=400)

    # ✅ Save new user with hashed password
    hashed_password = make_password(raw_password)
    new_user = {
        "username": username,
        "phnumber": phnumber,
        "email": email,
        "password": hashed_password,
    }

    db.child("user_login_details").child(email_key).set(new_user)

    return JsonResponse({"message": "Signup successful"}, status=201)

@csrf_exempt
def login_user(request):
    if request.method != "POST":
        return JsonResponse({"error": "Only POST allowed"}, status=405)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    email = data.get("email")
    raw_password = data.get("password")

    if not email or not raw_password:
        return JsonResponse({"error": "Email and password are required"}, status=400)

    # ✅ Use email_key instead of looping
    email_key = email.replace(".", "_")
    user = db.child("user_login_details").child(email_key).get().val()

    if not user:
        return JsonResponse({"error": "User not found"}, status=404)

    hashed_password = user.get("password")
    if check_password(raw_password, hashed_password):
        return JsonResponse({"message": "Login successful"}, status=200)

    return JsonResponse({"error": "Invalid password"}, status=401)





@csrf_exempt
def signup_org(request):
    if request.method != "POST":
        return JsonResponse({"error": "Only POST allowed"}, status=405)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    serializer = OrgSignupSerializer(data=data)
    if not serializer.is_valid():
        return JsonResponse({"error": serializer.errors}, status=400)

    org_name = serializer.validated_data["org_name"]
    phnumber = serializer.validated_data["phnumber"]
    email = serializer.validated_data["email"]
    org_type = serializer.validated_data["org_type"]
    license_number = serializer.validated_data["license_number"]
    raw_password = serializer.validated_data["password"]

    # ✅ Use email as key
    email_key = email.replace(".", "_")

    # Check for duplicates directly in DB
    if db.child("org_login_details").child(email_key).get().val():
        return JsonResponse({"error": "Email already exists"}, status=400)

    all_orgs = db.child("org_login_details").get().val() or {}
    for org in all_orgs.values():
        if org.get("org_name") == org_name:
            return JsonResponse({"error": "Organization name already exists"}, status=400)
        if org.get("phnumber") == phnumber:
            return JsonResponse({"error": "Phone number already exists"}, status=400)
        if org.get("license_number") == license_number:
            return JsonResponse({"error": "License/Registration number already exists"}, status=400)

    # Save with hashed password
    new_org = {
        "org_name": org_name,
        "phnumber": phnumber,
        "email": email,
        "org_type": org_type,
        "license_number": license_number,
        "password": make_password(raw_password),
    }
    db.child("org_login_details").child(email_key).set(new_org)

    return JsonResponse({"message": "Organization signup successful"}, status=201)



@csrf_exempt
def login_org(request):
    if request.method != "POST":
        return JsonResponse({"error": "Only POST allowed"}, status=405)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    serializer = OrgLoginSerializer(data=data)
    if not serializer.is_valid():
        return JsonResponse({"error": serializer.errors}, status=400)

    email = serializer.validated_data["email"]
    raw_password = serializer.validated_data["password"]

    # Use email as key
    email_key = email.replace(".", "_")
    org = db.child("org_login_details").child(email_key).get().val()

    if not org:
        return JsonResponse({"error": "Organization not found"}, status=404)

    hashed_password = org.get("password")
    if not hashed_password or not check_password(raw_password, hashed_password):
        return JsonResponse({"error": "Invalid password"}, status=401)

    return JsonResponse({"message": "Organization login successful"}, status=200)

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

    # Validate request data
    serializer = ResetPasswordSerializer(data=data)
    if not serializer.is_valid():
        return JsonResponse({"errors": serializer.errors}, status=400)

    email = serializer.validated_data["email"]
    otp = serializer.validated_data["otp"]
    new_password = serializer.validated_data["new_password"]  

    # Ensure password is hashed (in case serializer didn’t hash)
    if not new_password.startswith("pbkdf2_"):
        new_password = make_password(new_password)

    email_key = email.replace(".", "_")

    # Fetch OTP data
    otp_data = db.child("password_resets").child(email_key).get().val()
    if not otp_data:
        return JsonResponse({"error": "No OTP found or expired"}, status=400)

    if int(time.time()) > otp_data.get("expiry", 0):
        db.child("password_resets").child(email_key).remove()
        return JsonResponse({"error": "OTP expired. Request again."}, status=400)

    if str(otp_data.get("otp")) != str(otp):
        return JsonResponse({"error": "Invalid OTP"}, status=400)

    if not otp_data.get("verified", False):
        return JsonResponse({"error": "OTP not verified yet"}, status=400)

    # ✅ Update password in whichever section user belongs
    updated = False
    for section in ["user_login_details", "org_login_details", "admin_login_details"]:
        if db.child(section).child(email_key).get().val():
            db.child(section).child(email_key).update({"password": new_password})
            updated = True
            break

    if not updated:
        return JsonResponse({"error": "Account not found"}, status=404)

    # Remove OTP
    db.child("password_resets").child(email_key).remove()

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