import jwt
from django.conf import settings

def generating_jwt_token(payload):
    try:
        return jwt.encode(
            payload,
            settings.SECRET_KEY,
            'HS256'
        )
    except jwt.exceptions as e:
        return None


def decoding_jwt_token(token):
    try:
        decoded = jwt.decode(
            jwt=token.split()[1],
            key=settings.SECRET_KEY,
            algorithms=['HS256'],
        )
        return decoded
    except jwt.exceptions:
        return None


