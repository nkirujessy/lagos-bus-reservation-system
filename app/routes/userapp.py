# user
from flask import session, redirect, render_template, Blueprint, request

from app.helpers.util import app_config
from app.models.routemodel import routes
from app.models.settingsmodel import settings
from app.models.ticketmodel import ticket
from app.models.usersmodel import users

user_app_route = Blueprint('user_app_route', __name__,template_folder='templates')
from app import app, db

from app.models.reservationmodel import reservation
from app.models.transactionmodel import transaction
@user_app_route.route("/app/overview")
def user_dashboard():
    path = "Dashboard"
    active_route = request.path
    user = session.get('id')
    if not session.get('user'):
        return redirect('/')

    reservations = reservation.query.filter_by(userId=user).count()

    transactions = transaction.query.filter_by(userId=user).count()
    active_tickets = reservation.query.filter_by(userId=user, status=1).count()


    return render_template("dashboard/user/index.html", route=active_route, path=path, reserve_count=reservations, trans_count=transactions, tickets_count=active_tickets)
@user_app_route.route("/app/reservations")
def user_reservation():
    if not session.get('user'):
        return redirect('/')
    path = "Reservations"
    active_route = request.path
    user = session.get('id')
    reservations = reservation.query.filter(reservation.userId == user).join(ticket).all()
    currency= app_config().currency
    return render_template("dashboard/user/user-reservations.html",reserve_list=reservations,route=active_route, path=path, currency=currency)

@user_app_route.route("/app/profile")
def user_profile():
    if not session.get('user'):
        return redirect('/')
    path = "Profile"
    active_route = request.path
    return render_template("dashboard/user/user-dashboard-profile.html",route=active_route, path=path)

@user_app_route.route("/app/account")
def user_account():
    if not session.get('user'):
        return redirect('/')
    path = "Account"
    active_route = request.path
    user = users.query.filter(users.id==session.get('id')).first()
    return render_template("dashboard/user/user-dashboard-settings.html",route=active_route, path=path, user=user)
