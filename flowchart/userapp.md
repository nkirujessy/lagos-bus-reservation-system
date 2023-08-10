op2=>operation: from flask import session, redirect, render_template, Blueprint, request
op4=>operation: from app.helpers.util import app_config
op6=>operation: from app.models.routemodel import routes
op8=>operation: from app.models.settingsmodel import settings
op10=>operation: from app.models.ticketmodel import ticket
op12=>operation: from app.models.usersmodel import users
op14=>operation: user_app_route = Blueprint('user_app_route', __name__, template_folder='templates')
op16=>operation: from app import app, db
op18=>operation: from app.models.reservationmodel import reservation
op20=>operation: from app.models.transactionmodel import transaction
st23=>start: start user_dashboard
io25=>inputoutput: input:
op28=>operation: path = 'Dashboard'
op30=>operation: active_route = request.path
op32=>operation: user = session.get('id')
cond35=>condition: if (not session.get('user'))
io42=>inputoutput: output:  redirect('/')
e40=>end: end function return
op48=>operation: reservations = reservation.query.filter_by(userId=user).count()
op50=>operation: transactions = transaction.query.filter_by(userId=user).count()
op52=>operation: active_tickets = reservation.query.filter_by(userId=user, status=1).count()
io57=>inputoutput: output:  render_template('dashboard/user/index.html', route=active_route, path=path, reserve_count=reservations, trans_cou
nt=transactions, tickets_count=active_tickets)
e55=>end: end function return

op2->op4
op4->op6
op6->op8
op8->op10
op10->op12
op12->op14
op14->op16
op16->op18
op18->op20
op20->st23
st23->io25
io25->op28
op28->op30
op30->op32
op32->cond35
cond35(yes)->io42
io42->e40
cond35(no)->op48
op48->op50
op50->op52
op52->io57
io57->e55
