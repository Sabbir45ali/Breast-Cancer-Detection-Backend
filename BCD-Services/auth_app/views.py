import json
import random
import time
import os
import sys

from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import User
from django.core.mail import send_mail

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from firebase_admin import auth as firebase_auth
from firebase_config import db, firebase, admin_auth

from .serializers import (
    SignupSerializer, LoginSerializer,
    OrgSignupSerializer, OrgLoginSerializer,
    VerifyOTPSerializer, ResetPasswordSerializer, ForgotPasswordSerializer,
)

# Add project root for firebase_config
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(BASE_DIR)
from firebase_config import db, firebase, admin_auth


import json
import random
import time
import string
from datetime import timedelta
from django.conf import settings
from django.core.mail import send_mail
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from firebase_admin import auth as firebase_auth
from .serializers import SignupSerializer, LoginSerializer, OrgSignupSerializer, OrgLoginSerializer, VerifyOTPSerializer, ResetPasswordSerializer, ForgotPasswordSerializer
import sys, os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(BASE_DIR)
from firebase_config import db

# ---------------- SIGNUP USER ----------------
@csrf_exempt
@api_view(["POST"])
@permission_classes([AllowAny])
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

    email_key = email.replace(".", "_")

    existing_user = db.child("user_login_details").child(email_key).get().val()
    if existing_user:
        return JsonResponse({"error": "Email already exists"}, status=400)

    all_users = db.child("user_login_details").get().val() or {}
    for user in all_users.values():
        if user.get("username") == username:
            return JsonResponse({"error": "Username already exists"}, status=400)
        if user.get("phnumber") == phnumber:
            return JsonResponse({"error": "Phone number already exists"}, status=400)

    hashed_password = make_password(raw_password)
    new_user = {
        "username": username,
        "phnumber": phnumber,
        "email": email,
        "password": hashed_password,
    }
    db.child("user_login_details").child(email_key).set(new_user)

    try:
        # Create Firebase user
        firebase_user = firebase_auth.create_user(
            email=email,
            password=raw_password,
            display_name=username,
            phone_number=f"+91{phnumber}" if phnumber else None
        )

        # Store extra data in Firebase Realtime DB
        db.child("user_login_details").child(email_key).update({
            "firebase_uid": firebase_user.uid
        })

        # Create Django user if not exists
        django_user, created = User.objects.get_or_create(
            username=email,
            defaults={"email": email}
        )
        if created:
            django_user.set_password(raw_password)
            django_user.save()

        return JsonResponse({"message": "Signup successful", "brr": firebase_user.uid}, status=201)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


# ---------------- LOGIN USER ----------------
@csrf_exempt
@api_view(["POST"])
@permission_classes([AllowAny])
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

    email_key = email.replace(".", "_")
    user = db.child("user_login_details").child(email_key).get().val()

    if not user:
        return JsonResponse({"error": "User not found"}, status=404)

    hashed_password = user.get("password")
    if not check_password(raw_password, hashed_password):
        return JsonResponse({"error": "Invalid password"}, status=401)

    try:
        # Authenticate with Firebase
        firebase_user = firebase_auth.get_user_by_email(email)
        uid = firebase_user.uid

        # Ensure Django user exists
        django_user, created = User.objects.get_or_create(
            username=email,
            defaults={"email": email}
        )
        if created:
            django_user.set_password(raw_password)
            django_user.save()

        refresh = RefreshToken.for_user(django_user)

        return JsonResponse({
            "message": "Login successful",
            "brr": uid,
            "access": str(refresh.access_token),
            "refresh": str(refresh)
        }, status=200)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=401)


# ---------------- SIGNUP ORG ----------------
@csrf_exempt
@api_view(["POST"])
@permission_classes([AllowAny])
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

    email_key = email.replace(".", "_")

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

    hashed_password = make_password(raw_password)
    new_org = {
        "org_name": org_name,
        "phnumber": phnumber,
        "email": email,
        "org_type": org_type,
        "license_number": license_number,
        "password": hashed_password,
    }
    db.child("org_login_details").child(email_key).set(new_org)

    try:
        # Create Firebase user
        firebase_user = firebase_auth.create_user(
            email=email,
            password=raw_password,
            display_name=org_name,
            phone_number=f"+91{phnumber}" if phnumber else None
        )

        # Store extra data in Firebase Realtime DB
        db.child("org_login_details").child(email_key).update({
            "firebase_uid": firebase_user.uid
        })

        # Create Django user if not exists
        django_user, created = User.objects.get_or_create(
            username=email,
            defaults={"email": email}
        )
        if created:
            django_user.set_password(raw_password)
            django_user.save()

        return JsonResponse({"message": "Organization signup successful", "brr": firebase_user.uid}, status=201)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


# ---------------- LOGIN ORG ----------------
@csrf_exempt
@api_view(["POST"])
@permission_classes([AllowAny])
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

    email_key = email.replace(".", "_")
    org = db.child("org_login_details").child(email_key).get().val()

    if not org:
        return JsonResponse({"error": "Organization not found"}, status=404)

    hashed_password = org.get("password")
    if not hashed_password or not check_password(raw_password, hashed_password):
        return JsonResponse({"error": "Invalid password"}, status=401)

    try:
        # Authenticate with Firebase
        firebase_user = firebase_auth.get_user_by_email(email)
        uid = firebase_user.uid

        # Ensure Django user exists
        django_user, created = User.objects.get_or_create(
            username=email,
            defaults={"email": email}
        )
        if created:
            django_user.set_password(raw_password)
            django_user.save()

        refresh = RefreshToken.for_user(django_user)

        return JsonResponse({
            "message": "Organization login successful",
            "brr": uid,
            "access": str(refresh.access_token),
            "refresh": str(refresh)
        }, status=200)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=401)


# ---------------- REFRESH TOKEN ----------------
from rest_framework_simplejwt.views import TokenRefreshView

@csrf_exempt
@api_view(["POST"])
@permission_classes([AllowAny])
def refresh_token(request):
    return TokenRefreshView.as_view()(request._request)

#-------------------- PROTECTED SITE (EXAMPLE) ----------------
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def protected_site(request):
    user = request.user
    return JsonResponse({
        "message": "You have access to this protected site!",
        "user_email": user.email
    }, status=200)

#----------------------- ADMIN LOGIN ----------------
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
