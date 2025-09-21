import os
from decouple import config
from django.conf import settings

import pyrebase
import firebase_admin
from firebase_admin import credentials, auth as admin_auth

# ------------------------------
# Pyrebase (client SDK) — Realtime DB & Storage
# ------------------------------
firebase_config = {
    "apiKey": config("FIREBASE_API_KEY"),
    "authDomain": config("FIREBASE_AUTH_DOMAIN"),
    "databaseURL": config("FIREBASE_DB_URL"),
    "projectId": config("FIREBASE_PROJECT_ID"),
    "storageBucket": config("FIREBASE_STORAGE_BUCKET"),
    "messagingSenderId": config("FIREBASE_MESSAGING_SENDER_ID"),
    "appId": config("FIREBASE_APP_ID"),
    "measurementId": config("FIREBASE_MEASUREMENT_ID"),
}

firebase = pyrebase.initialize_app(firebase_config)
db = firebase.database()
storage = firebase.storage()

# ------------------------------
# Firebase Admin SDK (secure server-side)
# ------------------------------
cred_path = os.path.join(settings.BASE_DIR, "firebase-key.json")

if not firebase_admin._apps:
    try:
        # Try with local key file
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred)
    except Exception:
        # Fallback: use GOOGLE_APPLICATION_CREDENTIALS env var if set
        try:
            firebase_admin.initialize_app()
        except Exception as e:
            raise RuntimeError(
                f"Failed to initialize Firebase Admin SDK. "
                f"Provide firebase-key.json or set GOOGLE_APPLICATION_CREDENTIALS. Error: {e}"
            )

# Expose admin auth for imports
admin_auth = admin_auth
