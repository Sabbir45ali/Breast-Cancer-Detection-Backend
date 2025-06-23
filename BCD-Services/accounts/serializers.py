from rest_framework import serializers
from django.core.validators import RegexValidator
from firebase_config import db
import re
from .models import ImageUpload


class PersonalDetailsSerializer(serializers.Serializer):
    # Create a unique ID if not provided
    User_id = serializers.CharField(required=False)

    # All other fields
    First_Name = serializers.CharField(max_length=255)
    Middle_Name = serializers.CharField(max_length=255, required=False, allow_blank=True, allow_null=True)
    Last_Name = serializers.CharField(max_length=255)

    Phone_no = serializers.CharField(
        max_length=20,
        validators=[
            RegexValidator(regex=r'^\+?\d{10,13}$', message="Enter a valid phone number.")
        ]
    )

    Mail_id = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    # Validate password 
    def validate_password(self, value):
        errors = []
        if len(value) < 8:
            errors.append("Password must be at least 8 characters long.")
        if not re.search(r"[a-z]", value):
            errors.append("Password must contain at least one lowercase letter.")
        if not re.search(r"[A-Z]", value):
            errors.append("Password must contain at least one uppercase letter.")
        if not re.search(r"\d", value):
            errors.append("Password must contain at least one digit.")
        if not re.search(r"[@$!%*?&]", value):
            errors.append("Password must contain at least one special character (@$!%*?&).")
        if errors:
            raise serializers.ValidationError(errors)
        return value

    # Validate unique Phone number
    def validate_Phone_no(self, value):
        # 1. Enforce valid phone number format: +91XXXXXXXXXX or just 10-13 digits
        regex = r'^\+?\d{10,12}$'
        validator = RegexValidator(regex=regex, message="Enter a valid phone number.")
        validator(value)  # Manually apply

        # 2. Check for uniqueness from Firebase
        users = db.child("personal_details").get()
        if users.each():
            for user in users.each():
                user_data = user.val()
                if user_data and user_data.get("Phone_no") == value:
                    raise serializers.ValidationError("Phone number already exists.")

        return value


class ImageUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageUpload
        fields = ['title', 'image']
