"""
Marshmallow schemas for post-requests structure validation.
camelcase naming style is required becuase of the post requests styling.
"""
from typing import List
from marshmallow import Schema, fields, post_load

class Event:
    """Single event class"""
    def __init__(self, eventName: str, metadata: dict = None, timestampUTC: int = 0):
        self.eventName = eventName
        self.metadata = metadata
        self.timestampUTC = timestampUTC


class EventSchema(Schema):
    """Validation schema for the Event class"""
    eventName = fields.String(required=True)
    metadata = fields.Dict()
    timestampUTC = fields.Integer(strict=True)
    @post_load
    def create_object(self, data, **kwargs):
        """Create a single Event object"""
        return Event(**data)


class UserEvents:
    """Events assigned to specific user class"""
    def __init__(self, userId: str, events: List[Event]):
        self.userId = userId
        self.events = events


class UserEventsSchema(Schema):
    """Validation schema for the UserEvents class"""
    userId = fields.Str(required=True)
    events = fields.List(fields.Nested(EventSchema), required=True)
    @post_load
    def create_object(self, data, **kwargs):
        """Create a single UserEvents object"""
        return UserEvents(**data)


class Alias:
    """Class storing information for different ussers linkage"""
    def __init__(self, newUserId: str, originalUserId: str, timestampUTC: int = 0):
        self.newUserId = newUserId
        self.originalUserId = originalUserId
        self.timestampUTC = timestampUTC


class AliasSchema(Schema):
    """Validation schema for the Alias class"""
    newUserId = fields.String(required=True)
    originalUserId = fields.String(required=True)
    timestampUTC = fields.Integer(strict=True)
    @post_load
    def create_object(self, data, **kwargs):
        """Create a single Alias object"""
        return Alias(**data)


class Profile:
    """Single user profile class"""
    def __init__(self, userId: str, attributes: dict = None, timestampUTC: int = 0):
        self.userId = userId
        self.attributes = attributes
        self.timestampUTC = timestampUTC


class ProfileSchema(Schema):
    """Validation schema for the Profile class"""
    userId = fields.Str(required=True)
    attributes = fields.Dict()
    timestampUTC = fields.Integer(strict=True)
    @post_load
    def create_object(self, data, **kwargs):
        """create a single Profile object"""
        return Profile(**data)
