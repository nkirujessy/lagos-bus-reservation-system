from flask import Blueprint, render_template, request, jsonify, session, redirect
from sqlalchemy.orm import lazyload, joinedload
from werkzeug.security import check_password_hash

from app import db, app
from app.models.usersmodel import users

from app.models.reservationmodel import reservation
from app.models.routemodel import routes
from app.models.usersmodel import users
from app.models.ticketmodel import ticket
from app.models.busmodel import bus
from app.models.transactionmodel import transaction
admin_app_route = Blueprint('admin_app_route', __name__, template_folder='templates')


@admin_app_route.route('/super/login_process', methods=['GET', 'POST'])
def login_process():

    msg = ''
    status = False
    if request.method == 'POST':
        email = request.form['email']
    password = request.form['password']
    role = request.form['role']

    if not email:
        msg = 'Email is required'
    elif not password:
        msg = 'Password is required'
    user = db.one_or_404(db.select(users).filter_by(email=email))

    if user:
        if check_password_hash(user.password, password) and user.role == role:
            session[role] = True
            session['id'] = user.id
            session['email'] = user.email
            session['fullname'] = user.fullname
            msg = 'Login successful'
            status = True
    else:
        msg = 'Incorrect login details'
        status = False

    return jsonify({
            'message': msg,
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

@admin_app_route.route('/admin/ticket/list')
def admin_ticket_list():
    if not session.get('admin'):
        return redirect('/admin/login')
    path = 'Ticket List'
    active_route = request.path
    t_list = ticket.query.all()
    return render_template('dashboard/admin/ticket-list.html',ticket_list=t_list, path=path,route=active_route)
@admin_app_route.route('/admin/ticket/add')
def admin_ticket_add():
    if not session.get('admin'):
        return redirect('/admin/login')
    path = 'Ticket Add'
    active_route = request.path
    return render_template('dashboard/admin/ticket-add.html', path=path, route=active_route)




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
    return render_template('dashboard/admin/route-add.html', path=path, route=active_route)
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
