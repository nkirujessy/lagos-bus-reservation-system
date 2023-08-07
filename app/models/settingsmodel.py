import uuid

from sqlalchemy_serializer import SerializerMixin

from app import db
from sqlalchemy.sql import func

from app.models.reservationmodel import reservation
from app.models.transactionmodel import transaction
from sqlalchemy import UUID


class settings(db.Model,SerializerMixin):

    id = db.Column(db.String(36), primary_key=True, default=uuid.uuid4)
    appname = db.Column(db.String(225), nullable=False)
    currency = db.Column(db.String(225), nullable=False)



def __repr__(self):
    return f'<settings {self.id}>'
