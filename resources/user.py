from flask import request
from flask_restful import Resource
from http import HTTPStatus
from flask_jwt_extended import create_access_token
from flask_jwt_extended import  get_jwt_identity, jwt_required


from utils import hash_password
from models.user import User


class UserListResource(Resource):

    def post(self):
        json_data = request.get_json()

        username = json_data.get('username')
        email = json_data.get('email')
        non_hash_password = json_data.get('password')

        if User.get_by_username(username):
            return {'message': 'email already used'}, HTTPStatus.BAD_REQUEST

        if User.get_by_email(email):
            return {'message': 'email already used'}, HTTPStatus.BAD_REQUEST

        password = hash_password(non_hash_password)
        user = User(
            username=username,
            email=email,
            password=password,
            role="USER"
        )

        user.save()

        data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role
        }
        access_token = create_access_token(identity=data)
        return {'access_token': access_token}, HTTPStatus.CREATED


class UserResource(Resource):
    @jwt_required()
    def get(self, username: str):
        user = User.get_by_username(username=username)

        if user is None:
            return {'message': 'user not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if current_user["id"] == user.id:
            data = {
                'id': user.id,
                'username': user.username,
                'email': user.email,
            }

        else:
            data = {
                'id': user.id,
                'username': user.username,
            }

        return data, HTTPStatus.OK


class MeResource(Resource):
    @jwt_required()
    def get(self):
        user = User.get_by_id(id=get_jwt_identity()["id"])
        data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
        }
        return data, HTTPStatus.OK


class UserUpdateResource(Resource):
    @jwt_required()
    def put(self):
        data = request.get_json()
        # data contains : username, email, password
        current_user_id = get_jwt_identity()["id"]
        current_user : User = User.get_by_id(current_user_id)
        if data["username"] != "":
            current_user.username = data["username"]
        if data["email"] != "":
            current_user.email = data["email"]
        if data["password"] != "":
            current_user.password = hash_password(data["password"])
        current_user.save()

        new_data = {
            'id': current_user.id,
            'username': current_user.username,
            'email': current_user.email,
            'role': current_user.role
        }
        access_token = create_access_token(identity=new_data)
        return {
            "message": "User changed successfully",
            'access_token': access_token
        }, HTTPStatus.OK
