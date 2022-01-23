from http import HTTPStatus
from flask import request
from flask_restful import Resource
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_required,
    get_jti)
from utils import verify_hash
from models.user import User
import re

black_list = set()

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'


class TokenRessource(Resource):

    def post(self):

        json_data = request.get_json()
        email = json_data.get('email')
        password = json_data.get('password')
        if not re.fullmatch(regex, email):
            return {'Message': 'Email not valid'}, HTTPStatus.BAD_REQUEST
        user = User.get_by_email(email=email)
        if not user or not verify_hash(password, user.password):
            return {'message': 'username or password is incorrect'}, HTTPStatus.UNAUTHORIZED
        data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role
        }
        access_token = create_access_token(identity=data)
        refresh_token = create_refresh_token(identity=data)
        return {'access_token': access_token, 'refresh_token': refresh_token}, HTTPStatus.OK


class RefreshResource(Resource):
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user, fresh=False)
        return {access_token: access_token}, HTTPStatus.OK


class RevokeResource(Resource):
    @jwt_required()
    def post(self):
        jti = get_jti(request.headers["Authorization"][7:].encode())
        print(jti)
        black_list.add(jti)
        return {'message': 'Successfully logged out'}, HTTPStatus.OK

