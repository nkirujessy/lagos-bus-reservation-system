import uuid

from sqlalchemy_serializer import SerializerMixin

from app import db
from sqlalchemy.sql import func

from app.models.reservationmodel import reservation
from app.models.transactionmodel import transaction
from app.models.ticketmodel import ticket
from app.models.busmodel import bus
from sqlalchemy import UUID


class users(db.Model,SerializerMixin):
    __tablename__ = 'users'

    id = db.Column(db.String(36), primary_key=True, default=uuid.uuid4)
    fullname = db.Column(db.String(225), nullable=False)
    password = db.Column(db.String(225), nullable=False)
    email = db.Column(db.String(225), nullable=False)
    reservation = db.relationship(reservation, backref='users', lazy=True)
    transaction = db.relationship(transaction, backref='users', lazy=True)
    ticket = db.relationship(ticket, backref='users', lazy=True)
    bus = db.relationship(bus, backref='users', lazy=True)
    role = db.Column(db.String(225), nullable=False)
    code = db.Column(db.String(225), nullable=True)
    code_status = db.Column(db.Integer, nullable=True)
    status = db.Column(db.Integer, nullable=False)
    created = db.Column(db.DateTime(timezone=True), server_default=func.now())




def __repr__(self):
    return f'<users {self.id}>'
