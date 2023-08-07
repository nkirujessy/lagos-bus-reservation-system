import json

import requests
from flask import Blueprint, render_template, request
from sqlalchemy import and_

from app import app
from app.models.busmodel import bus
from app.models.locationmodel import location
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
        for value in data:
            tickets = ticket.query.filter(ticket.id==value['id']).join(routes).filter(ticket.routeId==value['routeId']).join(bus).join(busstop).all()


    return render_template('web/search.html', path=path,  response=tickets, departure=dept, adult=adult,children=children)
