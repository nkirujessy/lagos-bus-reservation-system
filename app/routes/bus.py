from flask import Blueprint, request, jsonify
from sqlalchemy import between
from marshmallow import Schema, fields
from app import db

from app.models.ticketmodel import ticket
from app.models.routemodel import routes
bus_route = Blueprint('bus_route', __name__,template_folder='templates')

class ticketSchema(Schema):
    class Meta:
        fields = ('id','name',	'description'	,'fee'	,'routeId',	'buseId	adult'	'children'	,'max_occupancy', 'available','availability_date','arrival_datetime',	'departure_datetime','status','created'	)

ticket_schema = ticketSchema()
tickets_schema = ticketSchema(many=True)

@bus_route.route("/api/bussearch", methods=['GET', 'POST'])
def buses_search_api():
    message = ''
    status = ''
    data = []
    path = 'Search Result'

    if request.method == 'POST':
        # and 'start_route' in request.form and 'end_route' in request.form and 'depature_date' in request.form and 'adult' in request.form and 'children' in request.form:
        start_route = request.form.get('start_route', None)
        end_route = request.form.get('end_route', None)
        dept_date = request.form.get('depature_date', None)
        adult = request.form.get('adult', None)
        children = request.form.get('children', None)

        if not start_route:
            message = 'Please select a from destination'
            status = False
        elif not end_route:
            message = 'Please select a to destination'
            status = False
        elif dept_date == '':
            message = 'Please select depature date'
            status = False
        elif adult == '0':
            message = 'Please add Adult passenger'
            status = False
        else:


           # tickets = db.session.execute(db.select(ticket).where(ticket.availability_date >= dept_date , ticket.adult >= adult , ticket.children >= children)).scalars()
           tickets = ticket.query.filter(ticket.availability_date == dept_date, ticket.adult == adult, ticket.children == children, ticket.status == 1).all()
           if tickets:
            status = True
            message = 'Tickets found.'
            data = tickets_schema.dump(tickets)
           else:
               status = False
               message = 'No ticket found.'

        return jsonify({
            'message': message,
            'status': status,
            'data': data

        })

#
