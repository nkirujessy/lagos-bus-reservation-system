from flask import render_template, Blueprint, request, redirect, session

import uuid
from app import db
from app.models.busmodel import bus
from app.models.reservationmodel import reservation
from app.models.routemodel import routes
from app.models.ticketmodel import ticket
from app.models.transactionmodel import transaction
from app.routes.control import id_generator

reserve_route = Blueprint('search_route', __name__,template_folder='templates')

@reserve_route.route("/checkout", methods=["POST", "GET"])
def checkout():
    path= "Checkout"
    if request.method == "GET":
        ticketId = request.args.get("ticket", None)
        tickets = ticket.query.filter(ticket.id==ticketId).join(routes).join(bus).first()
        if(not tickets):
            return redirect("/404")

    return render_template("web/reserve.html", path=path, tickets=tickets)

@reserve_route.route("/reserve", methods=["POST", "GET"])
def reservation():
    if request.method == "GET" and "ticket" in request.args and "adult" in request.args and "children" in request.args and "departure" in request.args:
        ticketId = request.args.get("ticket", None)
    adult = request.args.get("adult", None)
    children = request.args.get("children", None)
    departure = request.args.get("departure", None)
    reservation_number = id_generator()
    reference = uuid.uuid4()
    tickets = ticket.query.filter(ticket.id==ticketId).join(routes).join(bus).first()
    amount=0
    if(not tickets):
        return redirect("/404")
    else:
        amount = int(tickets.fee) * int(adult) + int(children)
        reserve= reservation(userId=session.get("id"),ticketId=ticketId, reservation_number=reservation_number, status=1, adult=adult,children=children)
        db.session.add(reserve)
        db.session.commit()
        transact = transaction(reference=reference,reservationId=reserve.id,userId=session.get("id"), amount=amount, status=1 )
        db.session.add(transact)
        db.session.commit()

        return redirect("/payment-success")


@reserve_route.route("/payment-success", methods=["POST", "GET"])
def payment_success():
    path= "Payment Successful"

    return render_template("web/payment-complete.html", path=path)
