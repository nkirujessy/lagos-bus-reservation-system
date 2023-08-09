from flask import render_template, Blueprint, request, redirect, session, jsonify

import uuid

from sqlalchemy import func

import app
from app import db
from app.helpers.util import app_config

from app.models.busmodel import bus
from app.models.reservationmodel import reservation
from app.models.routemodel import routes
from app.models.settingsmodel import settings
from app.models.ticketmodel import ticket
from app.models.transactionmodel import transaction
from app.models.usersmodel import users
from app.routes.control import id_generator

reserve_route = Blueprint('search_route', __name__, template_folder='templates')


@reserve_route.route("/checkout", methods=["POST", "GET"])
def checkout():
    path = "Checkout"
    if request.method == "GET":
        ticketId = request.args.get("ticket", None)
        adult = request.args.get("adult", None)
        children = request.args.get("children", None)
        busstop = request.args.get("children", None)
        currency = settings.query.first()
        tickets = ticket.query.filter(ticket.id == ticketId).join(routes).join(bus).first()
        if (not tickets):
            return redirect("/404")

    return render_template("web/reserve.html", path=path, tickets=tickets, adult=adult, children=children,
                           currency=currency.currency)


@reserve_route.route("/reserve", methods=["POST", "GET"])
def reserve_bus():
    if not session.get("user"):
        return redirect("/checkout")
    if request.method == "GET":
        ticketId = request.args.get("ticket", None)
        adult = request.args.get("adult", None)
        children = request.args.get("children", None)
        departure = request.args.get("departure", None)
        reservation_number = id_generator()
        reference = uuid.uuid4()
        user = session.get("id")
        tickets = ticket.query.filter(ticket.id == ticketId).join(routes).join(bus).first()

        if (not tickets):
            return redirect("/404")
        else:
            amount = (int(adult) + int(children)) * int(tickets.fee)
            init_capacity = (int(adult) + int(children))
            reserve = reservation(userId=user, ticketId=ticketId, reservation_number=reservation_number, status=1,
                                  adult=adult, children=children)
            db.session.add(reserve)
            db.session.commit()
            transact = transaction(reference=reference, reservationId=reserve.id, userId=session.get("id"),
                                   amount=amount, status=1)
            db.session.add(transact)
            db.session.commit()

            return redirect("/payment-success?ticket=" + ticketId + "&reservation=true&uid=" + reserve.id)


@reserve_route.route("/payment-success", methods=["POST", "GET"])
def payment_success():
    path = "Payment Successful"
    if request.method == "GET":
        ticketId = request.args.get("ticket", None)
        status = request.args.get("reservation", None)
        uid = request.args.get("uid", None)
        currency = app_config().currency
        tickets = ticket.query.filter(ticket.id == ticketId).first()
        reservations = reservation.query.filter(reservation.id == uid).join(transaction).join(ticket).join(
            users).first()
        if not tickets or not reservations:
            redirect("/")

        return render_template("web/payment-complete.html", path=path, result=reservations, currency=currency)


@reserve_route.route("/reservation/cancel", methods=["POST", "GET"])
def cancel_reservation():
    message = "Error Occurred"
    status = False
    if request.method == "GET":
        uid = request.args.get("uid", None)
        reservations = reservation.query.filter(reservation.id == uid).first()
        if not reservations:
            status = False
            message = "Reservation not found"
        elif reservations.checkin == 1:
            status = False
            message = "Reservation already checked in"
        elif reservations.status == 3:
            status = False
            message = "Reservation already cancelled"
        else:
            reservations.status = 3
            db.session.commit()
            status = True
            message = "Reservation cancelled"

    return jsonify({
        "message": message,
        "status": status
    })


@reserve_route.route("/reservation/checkin", methods=["POST", "GET"])
def checkin_reservation():
    message = "Error Occurred"
    status = False
    if request.method == "GET":
        id = request.args.get("id", None)
        reservations = reservation.query.filter(reservation.id == id).first()
        if not reservations:
            status = False
            message = "Reservation not found"
        elif reservations.checkin == 1:
            status = False
            message = "Reservation already checked in"
        else:
            reservations.checkin = 1
            reservations.status = 3
            db.session.commit()
            status = True
            message = "Reservation checked in"

    return jsonify({
        "message": message,
        "status": status
      })
