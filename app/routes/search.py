import json

import requests
from flask import Blueprint, render_template, request
from sqlalchemy import and_, func

from app import app, db
from app.helpers.util import app_config, time_diff
from app.models.busmodel import bus
from app.models.locationmodel import location
from app.models.reservationmodel import reservation
from app.models.routemodel import routes
from app.models.ticketmodel import ticket
from app.models.busstopmodel import busstop

search_route = Blueprint('search_route', __name__,template_folder='templates')


@app.route("/search")
def buses_search():
    path = 'Search Result'
    tickets = []
    if request.method == 'GET':
        dept = request.args.get('departure', None)
        adult = request.args.get('adult', None)
        children = request.args.get('children', None)
        response = request.args.get('response', None)
        data = json.loads(response)
        currency = app_config().currency

        for value in data:
            tickets = ticket.query.filter(ticket.id==value['id'], ticket.status==1).join(routes).filter(ticket.routeId==value['routeId']).join(bus).join(busstop).all()
            ticket_sum = db.session.query(func.sum(reservation.adult), func.sum(reservation.children)).filter(reservation.ticketId==value['id']).scalar()

            for res in tickets:
             interval = time_diff(res.departure_datetime, res.arrival_datetime)
             if ticket_sum == res.bus.max_occupancy:
                tickets =[]
                res.status=3
                db.session.commit()


        return render_template('web/search.html', path=path,  response=tickets, departure=dept, adult=adult,children=children, currency=currency, interval=interval)
