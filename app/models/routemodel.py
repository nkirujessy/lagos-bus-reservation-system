import uuid

from sqlalchemy.orm import backref

from app import db
from sqlalchemy.sql import func
class routes(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    start_routeId = db.Column(db.String(255),db.ForeignKey('location.id'), nullable=False)
    end_routeId = db.Column(db.String(255),db.ForeignKey('location.id'), nullable=False)
    ticket = db.relationship('ticket', backref=backref('routes'),  cascade="all, delete-orphan")
    status = db.Column(db.Integer, nullable=False)
    created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    # __table_args__ = (
    #     db.ForeignKeyConstraint(
    #         [start_routeId, end_routeId],
    #         ['location.id', 'location.id'],
    #     ),
    # )

    def __repr__(self):
        return f'<routes {self.id}>'
