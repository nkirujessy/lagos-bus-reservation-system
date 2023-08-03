import uuid

from app import db
from sqlalchemy.sql import func

from sqlalchemy import UUID

class transaction(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=uuid.uuid4)
    reference = db.Column(db.String(255), nullable=True)
    reservationId = db.Column(db.String(225), db.ForeignKey('reservation.id'), nullable=False)
    userId = db.Column(db.String(225), db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.Integer, nullable=False)
    created = db.Column(db.DateTime(timezone=True), server_default=func.now())


def __repr__(self):
    return f'<transaction {self.id}>'
