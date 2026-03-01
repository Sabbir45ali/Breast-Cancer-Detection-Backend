from firebase_admin import auth
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
class FirebaseAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            raise AuthenticationFailed("Authorization header required")
        try:
            token = auth_header.split(" ")[1]
            decoded = auth.verify_id_token(token)
            uid = decoded['uid']
            return (uid, None)
        except Exception:
            raise AuthenticationFailed("Invalid Token")