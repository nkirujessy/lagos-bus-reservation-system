import uuid

from sqlalchemy import func
from sqlalchemy.orm import backref
from sqlalchemy_serializer import SerializerMixin

from app import db


class busstop(db.Model,SerializerMixin):

    id = db.Column(db.String(36), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(225), nullable=False)
    description = db.Column(db.String(225), nullable=False)
    routeId=db.Column(db.String(255),db.ForeignKey('routes.id'), nullable=False)
    latitude=db.Column(db.String(255),nullable=False)
    longitude=db.Column(db.String(255),nullable=False)
    landmark=db.Column(db.String(255),nullable=False)
    address=db.Column(db.String(255),nullable=False)
    zipcode=db.Column(db.String(255),nullable=False)
    status = db.Column(db.Integer, nullable=False)
    created = db.Column(db.DateTime(timezone=True),server_default=func.now())

def __repr__(self):
    return f'<bus_stop {self.id}>'
