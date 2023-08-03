from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

from app import app










# @app.route('/routes')
# def routes():
#     path = 'Routes'
#     return render_template('web/routes.html', path=path)
#
#
# @app.route('/buses')
# def buses():
#     path = 'Buses'
#     return render_template('web/buses.html', path=path)
#
#
# @app.route('/tickets')
# def tickets():
#     path = 'Tickets'
#     return render_template('web/tickets.html', path=path)
#
#


# # user
# @app.route("/app/overview")
# def user_dashboard():
#     path = 'Dashboard'
#     if not session.get('user'):
#         return redirect('/')
#
#     return render_template("dashboard/user/index.html", path=path)

