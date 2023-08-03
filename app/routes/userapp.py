# user
from flask import session, redirect, render_template, Blueprint, request

user_app_route = Blueprint('user_app_route', __name__,template_folder='templates')
from app import app, db

from app.models.reservationmodel import reservation
from app.models.transactionmodel import transaction
@user_app_route.route("/app/overview")
def user_dashboard():
    path = "Dashboard"
    active_route = request.path
    if not session.get('user'):
        return redirect('/')
    reservations = reservation.query.count()

    transactions = transaction.query.count()
    active_tickets = reservation.query.count()


    return render_template("dashboard/user/index.html", route=active_route, path=path, reserve_count=reservations, trans_count=transactions, tickets_count=active_tickets)
@user_app_route.route("/app/reservations")
def user_reservation():
    path = "Reservations"
    active_route = request.path
    return render_template("dashboard/user/user-dashboard-booking.html",route=active_route, path=path)

@user_app_route.route("/app/profile")
def user_profile():
    path = "Profile"
    active_route = request.path
    return render_template("dashboard/user/user-dashboard-profile.html",route=active_route, path=path)

@user_app_route.route("/app/account")
def user_account():
    path = "Account"
    active_route = request.path
    return render_template("dashboard/user/user-dashboard-settings.html",route=active_route, path=path)
