import uuid

from app import db
from sqlalchemy.sql import func

from app.models.reservationmodel import reservation
from app.models.transactionmodel import transaction
from sqlalchemy import UUID


class Config(db.Model):
    __tablename__ = 'config'
    appname = db.Column(db.String(225), nullable=False)
    currency = db.Column(db.String(225), nullable=False)



def __repr__(self):
    return f'<config {self.id}>'
