import os

from flask_jwt_extended import (
    create_access_token,
    create_refresh_token
)
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)

token_secret_key = os.environ['TOKEN_SECRET_KEY']


class TokenSerializer:
    def __init__(self):
        pass

    @staticmethod
    def access_refresh_token(user_id):
        access_token = create_access_token(identity=user_id, fresh=True)
        refresh_token = create_refresh_token(user_id)

        return access_token, refresh_token

    @staticmethod
    def generate_token(data, expiration=600):
        token_serializer = Serializer(token_secret_key, expires_in=expiration)

        return token_serializer.dumps(data)

    @staticmethod
    def verify_token(token, data):
        token_serializer = Serializer(token_secret_key)

        try:
            toke_data = token_serializer.loads(token)
        except SignatureExpired:
            # Valid token, but expired
            return SignatureExpired
        except BadSignature:
            # Invalid token
            return BadSignature

        return toke_data == data

    @staticmethod
    def generate_auth_token(user_id, expiration=600):
        return TokenSerializer.generate_token({'id': user_id}, expiration)

    @staticmethod
    def verify_auth_token(token, user_id):
        return TokenSerializer.verify_token(token, {'id': user_id})
