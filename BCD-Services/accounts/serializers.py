from rest_framework import serializers
from .models import PersonalDetails, ImageUpload
from django.contrib.auth.hashers import make_password
import re
from django.core.validators import RegexValidator, EmailValidator


class PersonalDetailsSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  # Use lowercase 'password'

    class Meta:
        model = PersonalDetails
        fields = ['User_id', 'First_Name', 'Middle_Name', 'Last_Name', 'Phone_no', 'Mail_id', 'password', 'Profile_Pic']
        extra_kwargs = {'Password': {'write_only': True}}  # Keep this for model interaction (important!)

    def validate_mail_id(self, value):
        try:
            EmailValidator()(value)
        except serializers.ValidationError:
            raise serializers.ValidationError("Enter a valid email address.")
        return value

    def validate_password(self, value):
        """
        Custom validation for the password field.
        """
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

        return make_password(value)

    def validate_phone_no(self, value):
        """
        Custom validation for the phone number field.
        """
        try:
            RegexValidator(regex=r'^\+?\d{10,15}$', message="Enter a valid phone number.")(value)
        except serializers.ValidationError as e:
             raise serializers.ValidationError(e.detail)
        return value

    def create(self, validated_data):
        validated_data['Password'] = validated_data.pop('password')  # Use lowercase 'password'
        return PersonalDetails.objects.create(**validated_data)

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            instance.Password = validated_data.pop('password')  # Use lowercase 'password'
        instance.User_id = validated_data.get('User_id', instance.User_id)
        instance.First_Name = validated_data.get('First_Name', instance.First_Name)
        instance.Middle_Name = validated_data.get('Middle_Name', instance.Middle_Name)
        instance.Last_Name = validated_data.get('Last_Name', instance.Last_Name)
        instance.Phone_no = validated_data.get('Phone_no', instance.Phone_no)
        instance.Mail_id = validated_data.get('Mail_id', instance.Mail_id)
        instance.Profile_Pic = validated_data.get('Profile_Pic', instance.Profile_Pic)
        instance.save()
        return instance


class ImageUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageUpload
        fields = ['id', 'name', 'image']
