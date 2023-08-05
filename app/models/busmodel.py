import uuid

from sqlalchemy.orm import backref

from app import db
from sqlalchemy.sql import func


class bus(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(225), nullable=False)
    description = db.Column(db.String(225), nullable=False)
    image = db.Column(db.String(225), nullable=True)
    adult = db.Column(db.Integer, nullable=False, default=0)
    children = db.Column(db.Integer, nullable=False, default=0)
    max_occupancy = db.Column(db.Integer, nullable=False, default=0)
    status = db.Column(db.Integer, nullable=False)
    ticket = db.relationship('ticket', backref=backref('bus'))
    created = db.Column(db.DateTime(timezone=True), server_default=func.now())


def __repr__(self):
    return f'<buses {self.id}>'
