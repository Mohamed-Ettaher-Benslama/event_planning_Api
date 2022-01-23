from flask import request
from datetime import datetime
from flask_restful import Resource
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity, jwt_required
from models.event import Event
from http import HTTPStatus


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

        return {"data":response}, HTTPStatus.OK

    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        role = current_user['role']
        if role == 'ADMIN':
            event_data = request.get_json()
            event = Event(
                name=event_data['name'],
                description=event_data["description"],
                ticket_price=event_data["ticket_price"],
                date=datetime.strptime(event_data['date'],"%m/%d/%Y, %H:%M")
            )
            event.save()
            return {'Message': 'Event Added Successfully'}, HTTPStatus.OK
        else:
            return {'Message': 'Unauthorized acess'}, HTTPStatus.UNAUTHORIZED


class EventHandlingResource (Resource):
    @jwt_required()
    def delete(self, id):
        # id, username , email , role
        identity = get_jwt_identity()
        role=identity['role']
        if role=='ADMIN':
            event=Event.get_by_id(id)
            event.delete()
            return {'Message':'Event deleted sucessfuly'},HTTPStatus.OK
        else:
            return {'Message':'Unauthorized acess'},HTTPStatus.UNAUTHORIZED

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
            if data.get("name") is not None:
                event.name = data.get("name")
            if data.get("description") is not None:
                event.name = data.get("description")
            if data.get("ticket_price") is not None:
                event.name = data["ticket_price"]
            if data.get("date") is not None:
                event.name = datetime.strptime(data.get("date"), "%m/%d/%Y, %H:%M")
            event.save()
            return {'Message': 'Event with id '+str(id)+' Updatede Successfully'}, HTTPStatus.OK
        else:
            return {'Message': 'Unauthorized acess'}, HTTPStatus.UNAUTHORIZED


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




