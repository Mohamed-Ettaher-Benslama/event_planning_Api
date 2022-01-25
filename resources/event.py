from flask import request
from datetime import datetime
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required
from models.event import Event
from http import HTTPStatus
import re


class ListEventResource(Resource):
    @jwt_required()
    def get(self):
        events = Event.get_all()
        response = []
        for event in events:
            data = {
                'name': event.name,
                'description': event.description,
                'date': event.date.strftime("%m/%d/%Y, %H:%M"),
                'price': event.ticket_price
            }
            response.append(data)

        return {"data": response}, HTTPStatus.OK

    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        role = current_user['role']
        if role == 'ADMIN':
            event_data = request.get_json()
            try:
                date = datetime.strptime(event_data['date'], "%m/%d/%Y, %H:%M")
            except ValueError as err:
                return {'Message': 'Invalid Date format'}, HTTPStatus.BAD_REQUEST
            event = Event(
                name=event_data['name'],
                description=event_data["description"],
                ticket_price=event_data["ticket_price"],
                date=date
            )
            event.save()
            return {'Message': 'Event Added Successfully'}, HTTPStatus.OK
        else:
            return {'Message': 'Unauthorized acess'}, HTTPStatus.UNAUTHORIZED


class EventHandlingResource(Resource):
    @jwt_required()
    def delete(self, id):
        identity = get_jwt_identity()
        role = identity['role']
        if role == 'ADMIN':
            event = Event.get_by_id(id)
            if event is None:
                return {'Message': 'Event Not found'}, HTTPStatus.NOT_FOUND
            event.delete()
            return {'Message': 'Event deleted successfully'}, HTTPStatus.OK
        else:
            return {'Message': 'Unauthorized access'}, HTTPStatus.UNAUTHORIZED

    @jwt_required()
    def get(self, id):
        event = Event.get_by_id(id)
        data = {
            'name': event.name,
            'description': event.description,
            'date': event.date.strftime("%m/%d/%Y, %H:%M"),
            'price': event.ticket_price
        }
        return {'data': data}, HTTPStatus.OK

    @jwt_required()
    def put(self, id):
        identity = get_jwt_identity()
        role = identity['role']
        if role == 'ADMIN':
            event = Event.get_by_id(id)
            data = request.get_json()
            if data.get("date") is not None:
                try:
                    event.date = datetime.strptime(data.get("date"), "%m/%d/%Y, %H:%M")
                except ValueError as err:
                    return {'Message': 'Invalid Date format'}, HTTPStatus.BAD_REQUEST
            if data.get("name") is not None:
                event.name = data.get("name")
            if data.get("description") is not None:
                event.description = data.get("description")
            if data.get("ticket_price") is not None:
                event.ticket_price = data["ticket_price"]
            event.save()
            return {'Message': 'Event with id ' + str(id) + ' Updated Successfully'}, HTTPStatus.OK
        else:
            return {'Message': 'Unauthorized access'}, HTTPStatus.UNAUTHORIZED


class EventByNameResource(Resource):
    @jwt_required()
    def get(self, name: str):
        events = Event.get_by_name(name)
        response = []
        for event in events:
            data = {
                'name': event.name,
                'description': event.description,
                'date': event.date.strftime("%m/%d/%Y, %H:%M"),
                'price': event.ticket_price
            }
            response.append(data)
        return {'data': response}, HTTPStatus.OK
