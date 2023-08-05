from datetime import datetime
from pprint import pprint

from flask import Blueprint, request, jsonify
from sqlalchemy import between, or_
from marshmallow import Schema, fields
from app import db, app

from app.models.ticketmodel import ticket
from app.models.routemodel import routes
bus_route = Blueprint('bus_route', __name__,template_folder='templates')

class ticketSchema(Schema):
    class Meta:
        fields = ('id','name',	'description','fee','routeId','busId', 'available','availability_date','arrival_datetime',	'departure_datetime','status','created'	)

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
        dept_date = request.form.get('departure_date', None)
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
           check_route = routes.query.filter_by(start_routeId=start_route, end_routeId=end_route).all()
           tickets = []
           check_date= ''
           for ro in check_route:
               check_date =datetime.strptime(dept_date, '%d/%m/%Y').strftime('%Y-%m-%d')
               tickets = ticket.query.filter(or_(ticket.availability_date >= check_date , ticket.routeId == ro.id)).all()

           if tickets:
            status = True
            message = 'Search result found.'
            data = tickets_schema.dump(tickets)
            app.logger.info(check_date)
           else:
               status = False
               message = 'No ticket found.'

        return jsonify({
            'message': message,
            'status': status,
            'data': data

        })

#
