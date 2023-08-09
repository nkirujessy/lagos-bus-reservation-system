from flask import render_template, Blueprint

from app import app
from app.helpers.util import app_config
from app.models.ticketmodel import ticket

tickets_routes = Blueprint('tickets_roues', __name__,template_folder='templates')


@tickets_routes.route("/tickets")
def tickets():
    path="Tickets"
    data = ticket.query.all()
    currency = app_config().currency
    return render_template("web/tickets.html", path=path, result=data, currency=currency)

@tickets_routes.route("/routes")
def routess():
    path="Routes"
    data = ticket.query.all()
    return render_template("web/routes.html", path=path, result=data)
