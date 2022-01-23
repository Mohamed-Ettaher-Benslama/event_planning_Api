from flask import request
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required
from http import HTTPStatus

from models.event import Event
from models.event_subscription import EventSubscription


class ListSubscriptionsResource(Resource):
    @jwt_required()
    def get(self):
        identity = get_jwt_identity()
        user_id = identity['id']
        role = identity['role']
        if role == 'USER':
            event_subscriptions = EventSubscription.get_subscriptions_by_user_id(user_id)
            response = []
            for event_subscription in event_subscriptions:
                event = Event.get_by_id(event_subscription.eventid)
                data = {
                    'name': event.name,
                    'description': event.description,
                    'date': event.date.strftime("%m/%d/%Y, %H:%M"),
                    'price': event.ticket_price
                }
                response.append(data)
            return {'date': response}, HTTPStatus.OK
        else:
            return {'Message': 'UnAuthorized'}, HTTPStatus.UNAUTHORIZED

    @jwt_required()
    def post(self):
        identity = get_jwt_identity()
        role = identity['role']
        if role == 'USER':
            event_id = request.get_json().get('event_id')
            if event_id is None or Event.get_by_id(event_id) is None:
                return {'Message': 'Bad request event id is missing or event with id does not exist'}, HTTPStatus.BADREQUEST
            user_id = identity['id']
            event_subscription = EventSubscription(userid=user_id, eventid=event_id)
            event_subscription.save()
            return {'Message': 'Subscription Added Successfully'}, HTTPStatus.OK
        else:
            return {'Message': 'UnAuthorized'}, HTTPStatus.UNAUTHORIZED


class SubscriptionHandlingResource(Resource):
    @jwt_required()
    def delete(self, event_id):
        identity = get_jwt_identity()
        role = identity['role']
        if role == 'USER':
            user_id = identity['id']
            event_subscription: EventSubscription = EventSubscription.get_subscription_by_id(user_id, event_id)
            if event_subscription is None:
                return {'Message': 'Bad request event subscription does not exist'}, HTTPStatus.NOT_FOUND
            event_subscription.delete()
            return {'Message': 'Subscription Removed Successfully'}, HTTPStatus.OK
        else:
            return {'Message': 'UnAuthorized'}, HTTPStatus.UNAUTHORIZED
