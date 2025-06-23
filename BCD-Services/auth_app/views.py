from django.contrib.auth import authenticate, get_user_model
from django.http import JsonResponse
from rest_framework.authtoken.models import Token
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
import json

# Get the custom or default user model
User = get_user_model()

# Import your custom validators
from accounts.validator import (
    MinimumLengthValidator,
    UppercaseLetterValidator,
    LowercaseLetterValidator,
    DigitValidator,
    SymbolValidator
)

# Password validation helper
def validate_password(password):
    validators = [
        MinimumLengthValidator(),
        UppercaseLetterValidator(),
        LowercaseLetterValidator(),
        DigitValidator(),
        SymbolValidator()
    ]
    errors = []
    for validator in validators:
        try:
            validator.validate(password)
        except ValidationError as e:
            errors.append(e.messages[0])  # First error message
    return errors


@csrf_exempt  # ❗ Only for development/testing — use proper CSRF protection in production
def signup_view(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username = data.get("username")
            phnumber = data.get("number")
            email = data.get("email")
            password = data.get("password")

            if not all([username, email, password, phnumber]):
                return JsonResponse({"error": "All fields are required"}, status=400)

            if User.objects.filter(username=username).exists():
                return JsonResponse({"error": "Username already exists"}, status=400)
            if User.objects.filter(email=email).exists():
                return JsonResponse({"error": "Email already registered"}, status=400)

            password_errors = validate_password(password)
            if password_errors:
                return JsonResponse({
                    "error": "Password validation failed",
                    "details": password_errors
                }, status=400)

            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )

            token = Token.objects.create(user=user)

            return JsonResponse({
                "message": "User created successfully",
                "token": token.key
            }, status=201)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Only POST requests are allowed"}, status=405)


@csrf_exempt  # ❗ Only for development/testing
def login_view(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username = data.get("username")
            password = data.get("password")

            if not username or not password:
                return JsonResponse({"error": "Username and password are required"}, status=400)

            user = authenticate(username=username, password=password)
            if user is not None:
                token, _ = Token.objects.get_or_create(user=user)
                return JsonResponse({
                    "message": "Login successful",
                    "token": token.key
                }, status=200)
            else:
                return JsonResponse({"error": "Invalid credentials"}, status=401)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Only POST requests are allowed"}, status=405)
