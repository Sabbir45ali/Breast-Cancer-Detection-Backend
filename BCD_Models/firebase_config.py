import os
import firebase_admin
from firebase_admin import credentials, firestore, auth
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

if os.environ.get("FIREBASE_PRIVATE_KEY"):
    firebase_config = {
        "type": "service_account",
        "project_id": os.environ.get("FIREBASE_PROJECT_ID"),
        "private_key": os.environ.get("FIREBASE_PRIVATE_KEY").replace("\\n", "\n"),
        "client_email": os.environ.get("FIREBASE_CLIENT_EMAIL"),
    }
    cred = credentials.Certificate(firebase_config)
else:
    cred = credentials.Certificate(os.path.join(BASE_DIR, "serviceAccountKey.json"))

firebase_admin.initialize_app(cred)

db = firestore.client()