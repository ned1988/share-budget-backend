import json

import requests as requests
from authlib.jose import jwk, jwt
from authlib.jose.errors import ExpiredTokenError
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token
)
from flask_restplus import Resource, reqparse

from application import api
from model import db
from model.users import User
from utility.constants import Constants


def post_parameters(parser):
    parser.add_argument('userID', type=str, required=True, help="Apple sign in ID", location='form')
    parser.add_argument('identityToken', type=str, required=True, location='form')
    parser.add_argument(Constants.JSON.last_name, help='Last Name', location='form')
    parser.add_argument(Constants.JSON.first_name, help='First Name', location='form')


class LoginAppleResource(Resource):
    parser = api.parser()
    post_parameters(parser)

    @api.doc(parser=parser)
    def post(self):
        auth_key_content = requests.get('https://appleid.apple.com/auth/keys').content

        if auth_key_content is None:
            return Constants.error_reponse('keys are empty'), 401

        auth_keys_json = json.loads(auth_key_content)
        auth_keys = auth_keys_json['keys']
        if auth_keys is None or len(auth_keys) == 0:
            return Constants.error_reponse('keys are empty'), 401

        auth_key = auth_keys[0]
        key = jwk.loads(auth_key)

        parser = reqparse.RequestParser()
        post_parameters(parser)
        args = parser.parse_args()

        user_id = args['userID']
        identity_token = args['identityToken']

        try:
            jwt_claims = jwt.decode(s=identity_token, key=key)
            jwt_claims.validate()

            jwt_sub = jwt_claims['sub']
            if jwt_sub is None or jwt_sub != user_id:
                return Constants.error_reponse('wrong user')

            jwt_kid = jwt_claims.header['kid']
            apple_kid = auth_key['kid']
            if jwt_kid is None or apple_kid is None or jwt_kid != apple_kid:
                return Constants.error_reponse('kid is wrong'), 401

            jwt_aud = jwt_claims['aud']
            if jwt_aud is None or jwt_aud != 'denys.meloshyn.share-budget':
                return Constants.error_reponse('aud is wrong'), 401

            user = User.query.filter_by(apple_sign_in_id=user_id).first()
            if user is None:
                user = User(input_parameters={})
                user.is_email_approved = True
                user.apple_sign_in_id = user_id
                db.session.add(user)
                db.session.commit()

            user.update(new_value=args)
            user_json = user.to_json()
            user_json['accessToken'] = create_access_token(identity=user_id, fresh=True)
            user_json['refreshToken'] = create_refresh_token(user_id)

            return user_json
        except ExpiredTokenError:
            return Constants.error_reponse('expired JWT'), 401
