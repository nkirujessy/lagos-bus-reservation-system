import uuid


from app import db
from sqlalchemy.sql import func

from app.models.busmodel import bus

from app.models.routemodel import routes
class ticket(db.Model):

    id = db.Column(db.String(36), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(225), nullable=False)
    description = db.Column(db.String(225), nullable=False)
    fee = db.Column(db.String(225), nullable=False)
    routeId = db.Column(db.String(225), nullable=False)
    buseId = db.Column(db.Integer, nullable=False)
    reservation = db.relationship('reservation', backref='ticket', lazy=True)
    adult = db.Column(db.Integer, nullable=False)
    children = db.Column(db.Integer,nullable=False)
    max_occupancy = db.Column(db.Integer, nullable=False)
    available = db.Column(db.Integer, nullable=False)
    availability_date = db.Column(db.Integer, nullable=False)
    arrival_datetime = db.Column(db.Integer, nullable=False)
    departure_datetime = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Integer, nullable=False)
    created = db.Column(db.DateTime(timezone=True), server_default=func.now())


def __repr__(self):
    return f'<ticket {self.id}>'
