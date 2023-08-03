import uuid

from sqlalchemy import UUID

from app import db
from sqlalchemy.sql import func
from app.models.ticketmodel import ticket
class reservation(db.Model):

    __tablename__ = 'reservation'
    id = db.Column(db.String(36), primary_key=True, default=uuid.uuid4)
    userId = db.Column(db.String(225), db.ForeignKey('users.id'), nullable=False)
    ticketId = db.Column(db.String(225), db.ForeignKey(ticket.id), nullable=False)
    reservation_number = db.Column(db.String(225), nullable=False)
    status = db.Column(db.Integer, nullable=False)
    created = db.Column(db.DateTime(timezone=True), server_default=func.now())


def __repr__(self):
    return f'<reservation {self.id}>'
