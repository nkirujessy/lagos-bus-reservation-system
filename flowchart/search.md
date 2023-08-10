op2=>operation: import json
op4=>operation: import requests
op6=>operation: from flask import Blueprint, render_template, request
op8=>operation: from sqlalchemy import and_, func
op10=>operation: from app import app, db
op12=>operation: from app.helpers.util import app_config, time_diff
op14=>operation: from app.models.busmodel import bus
op16=>operation: from app.models.locationmodel import location
op18=>operation: from app.models.reservationmodel import reservation
op20=>operation: from app.models.routemodel import routes
op22=>operation: from app.models.ticketmodel import ticket
op24=>operation: from app.models.busstopmodel import busstop
op26=>operation: search_route = Blueprint('search_route', __name__, template_folder='templates')
st29=>start: start buses_search
io31=>inputoutput: input:
op34=>operation: path = 'Search Result'
op36=>operation: tickets = []
cond39=>condition: if (request.method == 'GET')
op43=>operation: dept = request.args.get('departure', None)
op45=>operation: adult = request.args.get('adult', None)
op47=>operation: children = request.args.get('children', None)
op49=>operation: response = request.args.get('response', None)
op51=>operation: data = json.loads(response)
op53=>operation: currency = app_config().currency
cond56=>condition: for value in data
op105=>operation: tickets = ticket.query.filter((ticket.id == value['id']), (ticket.status == 1)).join(routes).filter((ticket.routeId == valu
e['routeId'])).join(bus).join(busstop).all()
op107=>operation: ticket_sum = db.session.query(func.sum(reservation.adult), func.sum(reservation.children)).filter((reservation.ticketId ==
value['id'])).scalar()
cond110=>condition: for res in tickets
op131=>operation: interval = time_diff(res.departure_datetime, res.arrival_datetime)
cond134=>condition: if (ticket_sum == res.bus.max_occupancy)
op138=>operation: tickets = []
op140=>operation: res.status = 3
sub142=>subroutine: db.session.commit()
io154=>inputoutput: output:  render_template('web/search.html', path=path, response=tickets, departure=dept, adult=adult, children=children,
currency=currency, interval=interval)
e152=>end: end function return
e160=>end: end buses_search

op2->op4
op4->op6
op6->op8
op8->op10
op10->op12
op12->op14
op14->op16
op16->op18
op18->op20
op20->op22
op22->op24
op24->op26
op26->st29
st29->io31
io31->op34
op34->op36
op36->cond39
cond39(yes)->op43
op43->op45
op45->op47
op47->op49
op49->op51
op51->op53
op53->cond56
cond56(yes)->op105
op105->op107
op107->cond110
cond110(yes)->op131
op131->cond134
cond134(yes)->op138
op138->op140
op140->sub142
sub142->cond110
cond134(no)->cond110
cond110(no)->cond56
cond56(no)->io154
io154->e152
cond39(no)->e160
