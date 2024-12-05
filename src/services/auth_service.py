import jwt
import datetime
from flask import current_app

class AuthService:
    def __init__(self, db):
        self.db = db

    def generate_token(self, user_id, email, role):

        expiration_time = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)

        payload = {
            'user_id': user_id,
            'email': email,
            'role': role,
            'exp': expiration_time
        }
        
        token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')

        return token
    
    def decode_token(self, token):
        try:
            payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None