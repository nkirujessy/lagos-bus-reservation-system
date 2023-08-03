import uuid

from app import db
from sqlalchemy.sql import func
from sqlalchemy import UUID
class routes(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=uuid.uuid4)
    startLocationId = db.Column(db.String(255), nullable=False)
    endLocationId = db.Column(db.String(255), nullable=False)
    # ticket = db.relationship(ticket, backref='routes', lazy=True)
    status = db.Column(db.Integer, nullable=False)
    created = db.Column(db.DateTime(timezone=True),
                        server_default=func.now())

    def __repr__(self):
        return f'<routes {self.id}>'
