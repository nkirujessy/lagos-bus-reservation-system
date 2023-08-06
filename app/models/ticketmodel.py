import uuid

from sqlalchemy_serializer import SerializerMixin

from app import db
from sqlalchemy.sql import func

# from app.models.busmodel import bus
#
# from app.models.routemodel import routes
from app.models.reservationmodel import reservation
class ticket(db.Model,SerializerMixin):
    serialize_rules = ('-ticket.route.ticket')
    id = db.Column(db.String(36), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(225), nullable=False)
    description = db.Column(db.String(225), nullable=False)
    fee = db.Column(db.Integer, nullable=False)
    ticket_number = db.Column(db.String(225), nullable=False)
    routeId = db.Column(db.String(225), db.ForeignKey('routes.id'), nullable=False)
    busId = db.Column(db.String(225), db.ForeignKey('bus.id'), nullable=False)
    reservation = db.relationship(reservation,  backref='ticket', lazy=True)
    available = db.Column(db.Integer, nullable=False)
    availability_date = db.Column(db.Date(), nullable=False)
    arrival_datetime = db.Column(db.DateTime(timezone=True), nullable=False)
    departure_datetime = db.Column(db.DateTime(timezone=True), nullable=False)
    status = db.Column(db.Integer, nullable=False)
    created = db.Column(db.DateTime(timezone=True), server_default=func.now())


def __repr__(self):
    return f'<ticket {self.id}>'
