op2=>operation: from flask import render_template, Blueprint, request, redirect, session, jsonify
op4=>operation: import uuid                                                                      
op6=>operation: from sqlalchemy import func                                                      
op8=>operation: import app                                                                       
op10=>operation: from app import db                                                              
op12=>operation: from app.helpers.util import app_config
op14=>operation: from app.models.busmodel import bus
op16=>operation: from app.models.reservationmodel import reservation
op18=>operation: from app.models.routemodel import routes
op20=>operation: from app.models.settingsmodel import settings
op22=>operation: from app.models.ticketmodel import ticket
op24=>operation: from app.models.transactionmodel import transaction
op26=>operation: from app.models.usersmodel import users
op28=>operation: from app.routes.control import id_generator
op30=>operation: reserve_route = Blueprint('search_route', __name__, template_folder='templates')
st33=>start: start checkout
io35=>inputoutput: input:
op38=>operation: path = 'Checkout'
cond41=>condition: if (request.method == 'GET')
op45=>operation: ticketId = request.args.get('ticket', None)
op47=>operation: adult = request.args.get('adult', None)
op49=>operation: children = request.args.get('children', None)
op51=>operation: busstop = request.args.get('children', None)
op53=>operation: currency = settings.query.first()
op55=>operation: tickets = ticket.query.filter((ticket.id == ticketId)).join(routes).join(bus).first()
cond58=>condition: if (not tickets)
io65=>inputoutput: output:  redirect('/404')
e63=>end: end function return
io77=>inputoutput: output:  render_template('web/reserve.html', path=path, tickets=tickets, adult=adult, children=children, currency=currency
.currency)
e75=>end: end function return

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
op26->op28
op28->op30
op30->st33
st33->io35
io35->op38
op38->cond41
cond41(yes)->op45
op45->op47
op47->op49
op49->op51
op51->op53
op53->op55
op55->cond58
cond58(yes)->io65
io65->e63
cond58(no)->io77
io77->e75
cond41(no)->io77
