from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
import json

@csrf_exempt  # Temporarily disable CSRF for testing
def login_view(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username = data.get("username")
            password = data.get("password")

            user = authenticate(username=username, password=password)

            if user:
                login(request, user)
                return JsonResponse({"message": "Login successful", "username": user.username}, status=200)
            else:
                return JsonResponse({"error": "Invalid credentials"}, status=401)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

    return JsonResponse({"error": "Only POST requests are allowed"}, status=405)
