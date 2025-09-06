from rest_framework import serializers
from django.core.validators import validate_email
import re
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
# --- User serializers ---
class SignupSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, max_length=150)
    phnumber = serializers.CharField(required=True, max_length=15)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    def validate_email(self, value):
        try:
            validate_email(value)
        except Exception:
            raise serializers.ValidationError("Please enter a valid email address")
        return value

    def validate_phnumber(self, value):
        if not value.isdigit() or len(value) < 10 or len(value) > 15:
            raise serializers.ValidationError(
                "Phone number must be digits only and between 10-15 chars."
            )
        return value

    def validate_password(self, value):
        errors = []
        if len(value) < 8:
            errors.append("Password must be at least 8 characters long")
        if not re.search(r"[A-Z]", value):
            errors.append("Password must contain an uppercase letter")
        if not re.search(r"[a-z]", value):
            errors.append("Password must contain a lowercase letter")
        if not re.search(r"[0-9]", value):
            errors.append("Password must contain a digit")
        if not re.search(r"[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>\/?]", value):
            errors.append("Password must contain a special character")

        if errors:
            raise serializers.ValidationError(errors)
        return value


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)

# --- Organization serializers ---

class OrgSignupSerializer(serializers.Serializer):
    org_name = serializers.CharField(required=True, max_length=150)
    phnumber = serializers.CharField(required=True, max_length=15)
    email = serializers.EmailField(required=True)
    org_type = serializers.ChoiceField(
        choices=["lab", "hospital", "diagnostic_center", "clinic", "pharmacy"],
        required=True
    )
    license_number = serializers.CharField(required=True, max_length=50)
    password = serializers.CharField(write_only=True, required=True)

    # --- Validators ---
    def validate_email(self, value):
        try:
            validate_email(value)
        except Exception:
            raise serializers.ValidationError("Please enter a valid email address")
        return value

    def validate_phnumber(self, value):
        if not value.isdigit() or len(value) < 10 or len(value) > 15:
            raise serializers.ValidationError(
                "Phone number must be digits only and between 10-15 chars."
            )
        return value

    def validate_password(self, value):
        errors = []
        if len(value) < 8:
            errors.append("Password must be at least 8 characters long")
        if not re.search(r"[A-Z]", value):
            errors.append("Password must contain an uppercase letter")
        if not re.search(r"[a-z]", value):
            errors.append("Password must contain a lowercase letter")
        if not re.search(r"[0-9]", value):
            errors.append("Password must contain a digit")
        if not re.search(r"[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>\/?]", value):
            errors.append("Password must contain a special character")

        if errors:
            raise serializers.ValidationError(errors)
        return value


class OrgLoginSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)



class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    new_password = serializers.CharField(min_length=6, write_only=True)
    otp = serializers.CharField(max_length=6, write_only=True)  # OTP from user

    def validate_new_password(self, value):
        """
        Optional: Validate password strength like in signup
        """
        errors = []
        if len(value) < 8:
            errors.append("Password must be at least 8 characters long")
        if not re.search(r"[A-Z]", value):
            errors.append("Password must contain an uppercase letter")
        if not re.search(r"[a-z]", value):
            errors.append("Password must contain a lowercase letter")
        if not re.search(r"[0-9]", value):
            errors.append("Password must contain a digit")
        if not re.search(r"[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>\/?]", value):
            errors.append("Password must contain a special character")

        if errors:
            raise serializers.ValidationError(errors)

        return make_password(value)  # hash password before sending to Firebase

    def validate_otp(self, value):
        if not value.isdigit() or len(value) != 6:
            raise serializers.ValidationError("OTP must be a 6-digit number")
        return value
