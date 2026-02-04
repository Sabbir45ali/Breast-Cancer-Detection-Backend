import firebase_admin
from firebase_admin import credentials, auth, db
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

cred_path = os.path.join(
    BASE_DIR,
    "firebase-service-account.json"
)

if not firebase_admin._apps:
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(
        cred,
        {
            "databaseURL": "https://student-data-b6b79-default-rtdb.firebaseio.com/"
        }
    )

# Expose what apps need
firebase_auth = auth
firebase_db = db.reference()
