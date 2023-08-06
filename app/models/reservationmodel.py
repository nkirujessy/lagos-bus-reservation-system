import uuid

from sqlalchemy import UUID
from sqlalchemy_serializer import SerializerMixin

from app import db
from sqlalchemy.sql import func
from app.models.transactionmodel import transaction
class CustomSerializerMixin(SerializerMixin):
    serialize_types = (
        (UUID, lambda x: str(x)),
    )
class reservation(db.Model,SerializerMixin):

    __tablename__ = 'reservation'
    serialize_only = ('id', 'userId', 'ticketId', 'users','reservation_number','status','created')
    serialize_rules = ('-users.reservation.users','-ticket.reservation.ticket')

    id = db.Column(db.String(36), primary_key=True, default=uuid.uuid4)
    userId = db.Column(db.String(225), db.ForeignKey('users.id'), nullable=False)
    ticketId = db.Column(db.String(225), db.ForeignKey('ticket.id'), nullable=False)
    reservation_number = db.Column(db.String(225), nullable=False)
    adult = db.Column(db.Integer, nullable=False)
    children = db.Column(db.Integer, nullable=False)
    transaction = db.relationship(transaction, backref='reservation', lazy=True)
    status = db.Column(db.Integer, nullable=False)
    created = db.Column(db.DateTime(timezone=True), server_default=func.now())
#

def __repr__(self):
    return f'<reservation {self.id}>'
