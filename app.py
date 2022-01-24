from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api
from config import Config
from extention import db, jwt
from utils import hash_password
from http import HTTPStatus

from resources.user import UserListResource, UserResource, MeResource, UserUpdateResource, AdminResource
from resources.jwt import TokenRessource, RefreshResource, RevokeResource, black_list
from resources.event import ListEventResource, EventHandlingResource, EventByNameResource
from resources.subscription import SubscriptionHandlingResource, ListSubscriptionsResource


def create_app():
    application = Flask(__name__)
    application.config.from_object(Config)
    register_extensions(application)
    register_resources(application)
    return application


def register_extensions(app):
    db.app = app
    db.init_app(app)
    migrate = Migrate(app, db)
    jwt.init_app(app)

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blacklist(_, decrypted_token):
        jti = decrypted_token['jti']
        test = jti in black_list
        return test

def register_resources(app):
    api = Api(app)
    api.add_resource(UserListResource, '/registrate')
    api.add_resource(AdminResource, '/registrate/admin')
    api.add_resource(TokenRessource, '/login')
    api.add_resource(UserUpdateResource, '/users/update')
    api.add_resource(UserResource, '/users/<string:username>')
    api.add_resource(MeResource, "/me")
    api.add_resource(RefreshResource, "/refresh")

    api.add_resource(RevokeResource, '/revoke')
    api.add_resource(ListEventResource, '/events')
    api.add_resource(ListSubscriptionsResource, '/subscription')
    api.add_resource(SubscriptionHandlingResource, '/subscription/<int:event_id>')
    api.add_resource(EventHandlingResource, '/events/<int:id>')
    api.add_resource(EventByNameResource, '/events/<string:name>')


if __name__ == '__main__':
    print(hash_password("admin"))
    app = create_app()
    app.run()
