import random
import string

from flask import Blueprint, render_template, request, jsonify, session, redirect
from werkzeug.security import check_password_hash

from app import db, app
from app.models.usersmodel import users

from app.models.reservationmodel import reservation
from app.models.routemodel import routes
from app.models.usersmodel import users
from app.models.ticketmodel import ticket
from app.models.busmodel import bus
from app.models.transactionmodel import transaction
from app.models.locationmodel import location
admin_app_route = Blueprint('admin_app_route', __name__, template_folder='templates')


def id_generator(size=8, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
@admin_app_route.route('/super/login_process', methods=['GET', 'POST'])
def login_process():


 if request.method == 'POST':
     message = 'Error Occurred'
     status = False
     email = request.form['email']
     password = request.form['password']
     role = request.form['role']
     if not email:
         message = 'Email is required'
         status=False
     elif not password:
         message = 'Password is required'
         status = False
     else:
        user = db.one_or_404(db.select(users).filter_by(email=email))
        if user:
            if check_password_hash(user.password, password) and user.role == role:
                session[role] = True
                session['id'] = user.id
                session['email'] = user.email
                session['fullname'] = user.fullname
                message = 'Login successful'
                status = True
 # else:
 #    message = 'Incorrect login details'
 #    status = False
        return jsonify({
        'message': message,
        'status': status
    })




@admin_app_route.route('/admin/login')
def admin_login():
    path = 'Admin Login'
    return render_template('auth/admin-login.html', path=path)


@admin_app_route.route('/driver/login')
def driver_login():
    path = 'Driver Login'
    return render_template('auth/admin-login.html', path=path)
@admin_app_route.route('/admin/logout')
def admin_logout():
    session.pop('admin', None)
    session.pop('id', None)
    session.pop('email', None)
    return redirect('/admin/login')
@admin_app_route.route('/admin/overview')
def admin_overview():
    if not session.get('admin'):
        return redirect('/admin/login')
    path = 'Control Panel'
    active_route = request.path
    r_count = reservation.query.count()
    route_count = routes.query.count()
    users_count =  users.query.filter_by(role='user').count()
    ticket_count =  ticket.query.count()

    return render_template('dashboard/admin/index.html',ticket_count=ticket_count,users_count=users_count, reservation_count=r_count, route_count=route_count,path=path, route=active_route)


@admin_app_route.route('/admin/reservations/list')
def admin_reservations():
    if not session.get('admin'):
        return redirect('/admin/login')
    path = 'Reservations'
    active_route = request.path
    r_list = reservation.query.all()
    return render_template('dashboard/admin/reservations.html', reserve_list=r_list,path=path, route=active_route)
@admin_app_route.route('/admin/reservations/search')
def admin_reservation_search():
    if not session.get('admin'):
        return redirect('/admin/login')
    path = 'Search Reservation'
    active_route = request.path

    return render_template('dashboard/admin/reservations-search.html', path=path, route=active_route)

@admin_app_route.route('/admin/reservations/search/result')
def admin_reservation_search_result():
    if not session.get('admin'):
        return redirect('/admin/login')
    path = 'Reservation Search Result'
    active_route = request.path
    return render_template('dashboard/admin/reservations-search-result.html', path=path, route=active_route)
@admin_app_route.route('/admin/bus/list')
def admin_bus_list():
    if not session.get('admin'):
        return redirect('/admin/login')
    path = 'Bus List'
    active_route = request.path
    b_list = bus.query.all()

    return render_template('dashboard/admin/bus-list.html',bus_list=b_list,path=path, route=active_route)

@admin_app_route.route('/admin/bus/add')
def admin_bus_add():
    if not session.get('admin'):
        return redirect('/admin/login')
    path = 'Add Bus'
    active_route = request.path
    return render_template('dashboard/admin/bus-add.html', path=path, route=active_route)
@admin_app_route.route('/admin/bus/add_process', methods=['POST','GET'])
def admin_bus_add_process():
    status = False
    message = 'Error Occured'
    if not session.get('admin'):
        return redirect('/admin/login')
    if request.method == 'POST':
        bus_name = request.form['bus_name']
        capacity = request.form['max_occupancy']
        adult = request.form['adult']
        children = request.form['children']
        desc = request.form['description']
        status = 1

        if not bus_name:
            message = 'Bus number is required'
            status= False
        elif not capacity:
            message = 'Maximum occupancy is required'
            status = False


        else:
            newbus =  bus(name=bus_name,description=desc,max_occupancy=capacity, adult=adult, children=children,  status=status)
            db.session.add(newbus)
            db.session.commit()
            status = True
            message = 'Bus created.'
    elif request == 'POST':
        message = 'Please fill out the form !'

    return jsonify({
        'message': message,
        'status': status
    })

@admin_app_route.route('/admin/ticket/list')
def admin_ticket_list():
    if not session.get('admin'):
        return redirect('/admin/login')
    path = 'Ticket List'
    active_route = request.path
    # t_list = ticket.query.all()
    t_list = db.session.query(ticket).filter(ticket.routeId == routes.id, ticket.busId == bus.id).all()
    app.logger.info('Ticket Lit')
    return render_template('dashboard/admin/ticket-list.html',ticket_list=t_list, path=path,route=active_route)
@admin_app_route.route('/admin/ticket/add')
def admin_ticket_add():
    if not session.get('admin'):
        return redirect('/admin/login')
    path = 'Ticket Add'
    active_route = request.path
    routes_list = routes.query.filter_by(status=1).all()
    bus_list = bus.query.filter_by(status=1).all()
    return render_template('dashboard/admin/ticket-add.html', bus_list=bus_list,routes_list=routes_list, path=path, route=active_route)

@admin_app_route.route('/admin/ticket/add_process', methods=['POST','GET'])
def admin_ticket_add_process():
    status = False
    message = 'Error Occurred'
    if not session.get('admin'):
        return redirect('/admin/login')
    if request.method == 'POST':
        name = request.form['name']
        fee = request.form['fee']
        available = request.form['available']
        avail_date = request.form['availability_date']
        dept = request.form['departure_time']
        arrival = request.form['arrival_time']
        bus = request.form['bus']
        route = request.form['route']
        desc = request.form['description']
        status = 1
        ticket_number = id_generator()
        if not name:
            message = 'Ticket name is required'
            status= False
        elif not fee:
            message = 'Fee is required'
            status = False
        elif not int(fee):
            message = 'Fee should be number'
            status = False
        elif not available:
            message = 'Is ticket available should be selected'
            status = False
        elif not avail_date:
            message = 'Availability date is required'
            status = False
        elif not dept:
            message = 'Departure time is required'
            status = False
        elif not arrival:
            message = 'Arrival time is required'
            status = False
        elif not bus:
            message = 'Bus is required'
            status = False
        elif not route:
            message = 'Route is required'
            status = False
        elif not desc:
            message = 'Description is required'
            status = False


        else:
            data =  ticket(name=name,description=desc,fee=fee, ticket_number=ticket_number, routeId=route,busId=bus,available=available, availability_date=avail_date, arrival_datetime=arrival,departure_datetime=dept,  status=status)
            db.session.add(data)
            db.session.commit()
            status = True
            message = 'Ticket created.'
    elif request == 'POST':
        message = 'Please fill out the form !'

    return jsonify({
        'message': message,
        'status': status
    })


@admin_app_route.route('/admin/routes/list')
def admin_routes_list():
    if not session.get('admin'):
        return redirect('/admin/login')
    path = 'Routes List'
    active_route = request.path
    r_list = routes.query.all()
    return render_template('dashboard/admin/route-list.html' ,route_list=r_list, path=path, route=active_route)
@admin_app_route.route('/admin/routes/add')
def admin_routes_add():
    if not session.get('admin'):
        return redirect('/admin/login')
    path = 'Add Route'
    active_route = request.path
    locations = location.query.all()
    return render_template('dashboard/admin/route-add.html', locations=locations,path=path, route=active_route)
@admin_app_route.route('/admin/route/add_process', methods=['POST','GET'])
def admin_route_add_process():
    status = False
    message = 'Error Occured'
    if not session.get('admin'):
        return redirect('/admin/login')
    if request.method == 'POST':
        route_name = request.form['route_name']
        start = request.form['start_route']
        end = request.form['end_route']
        desc = request.form['description']
        status = 1

        if not route_name:
            message = 'Route name is required'
            status= False
        elif not start:
            message = 'Start Location is required'
            status = False
        elif not end:
            message = 'End Location is required'
            status = False


        else:
            data =  routes(name=route_name,description=desc,start_routeId=start, end_routeId=end, status=status)
            db.session.add(data)
            db.session.commit()
            status = True
            message = 'Route created.'
    elif request == 'POST':
        message = 'Please fill out the form !'

    return jsonify({
        'message': message,
        'status': status
    })
@admin_app_route.route('/admin/users')
def admin_users():
    if not session.get('admin'):
        return redirect('/admin/login')
    path = 'Users'
    active_route = request.path
    u_list =  users.query.all()
    return render_template('dashboard/admin/users.html', users_list=u_list, path=path, route=active_route)
@admin_app_route.route('/admin/transactions')
def admin_transactions():
    if not session.get('admin'):
        return redirect('/admin/login')
    path = 'Transactions'
    active_route = request.path
    t_list = transaction.query.all()
    return render_template('dashboard/admin/transactions.html',transaction_list=t_list, path=path, route=active_route)
@admin_app_route.route('/admin/settings')
def admin_settings():
    if not session.get('admin'):
        return redirect('/admin/login')
    path = 'Settings'
    active_route = request.path
    return render_template('dashboard/admin/settings.html', path=path, route=active_route)
@admin_app_route.route('/admin/profile')
def admin_profile():
    if not session.get('admin'):
        return redirect('/admin/login')
    path = 'Profile'
    active_route = request.path
    return render_template('dashboard/admin/profile.html', path=path, route=active_route)
