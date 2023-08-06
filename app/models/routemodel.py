import uuid

from sqlalchemy.orm import backref
from sqlalchemy_serializer import SerializerMixin

from app import db
from sqlalchemy.sql import func
class routes(db.Model,SerializerMixin):
    id = db.Column(db.String(36), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)

    start_routeId = db.Column(db.String(255),db.ForeignKey('location.id'), nullable=False)
    end_routeId = db.Column(db.String(255),db.ForeignKey('location.id'), nullable=False)
    start_route = db.relationship('location', foreign_keys=[start_routeId])
    end_route = db.relationship('location', foreign_keys=[end_routeId])
    ticket = db.relationship('ticket', backref=backref('routes'),  cascade="all, delete-orphan")
    status = db.Column(db.Integer, nullable=False)
    created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    # location_route = db.Table('location_route',
    #                 db.Column('start_routeId',db.String(255), db.ForeignKey('location.id'), nullable=False),
    #                 db.Column('end_routeId',db.String(255), db.ForeignKey('location.id'), nullable=False)
    #                 )
    def __repr__(self):
        return f'<routes {self.id}>'
