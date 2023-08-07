import uuid
from dataclasses import dataclass

from sqlalchemy import UUID
from sqlalchemy_serializer import SerializerMixin

from app import db
from sqlalchemy.sql import func

from app.models.routemodel import routes
class location(db.Model,SerializerMixin):
    id = db.Column(db.String(36), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(225), nullable=False)
    status = db.Column(db.Integer, nullable=False)
    created = db.Column(db.DateTime(timezone=True), server_default=func.now())

def __repr__(self):
    return f'<location {self.id}>'

