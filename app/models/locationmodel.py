import uuid
from dataclasses import dataclass

from sqlalchemy import UUID

from app import db
from sqlalchemy.sql import func
from app.models.routemodel import routes
class location(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=uuid.uuid4)
    location = db.Column(db.String(225), nullable=False)
    # start_route = db.relationship('routes',   foreign_keys=[routes.id],  backref='start_routeId', lazy=True)
    # end_route = db.relationship('routes',foreign_keys=[routes.id],  backref='end_routeId', lazy=True)
    status = db.Column(db.Integer, nullable=False)
    created = db.Column(db.DateTime(timezone=True), server_default=func.now())



def __repr__(self):
    return f'<location {self.id}>'
