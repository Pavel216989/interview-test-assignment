from marshmallow import Schema, fields, post_load
import datetime as dt
from typing import List

class Event:
    def __init__(self, eventName: str, metadata : dict = None, timestampUTC: int = 0):
        self.eventName = eventName
        self.metadata = metadata
        self.timestampUTC = timestampUTC


class EventSchema(Schema):
    eventName = fields.String(required=True)
    metadata = fields.Dict()
    timestampUTC = fields.Integer(strict=True)
    @post_load
    def create_object(self, data, **kwargs):
        return Event(**data)


class UserEvents:
    def __init__(self, userId: str, events: List[Event]):
        self.userId = userId
        self.events = events


class UserEventsSchema(Schema):
    userId = fields.Str(required=True)
    events = fields.List(fields.Nested(EventSchema), required = True)
    @post_load
    def create_object(self, data, **kwargs):
        return UserEvents(**data)


class Alias:
    def __init__(self, newUserId: str, originalUserId: str, timestampUTC: int = 0):
        self.newUserId = newUserId
        self.originalUserId = originalUserId
        self.timestampUTC = timestampUTC


class AliasSchema(Schema):
    newUserId = fields.String(required=True)
    originalUserId = fields.String(required=True)
    timestampUTC = fields.Integer(strict=True)
    @post_load
    def create_object(self, data, **kwargs):
        return Alias(**data)


class Profile:
    def __init__(self, userId: str, attributes: dict = None, timestampUTC: int = 0):
        self.userId = userId
        self.attributes = attributes
        self.timestampUTC = timestampUTC


class ProfileSchema(Schema):
    userId = fields.Str(required=True)
    attributes = fields.Dict()
    timestampUTC = fields.Integer(strict=True)
    @post_load
    def create_object(self, data, **kwargs):
        return Profile(**data)