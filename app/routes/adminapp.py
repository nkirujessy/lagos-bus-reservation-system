from flask import Blueprint, render_template, request, jsonify, session, redirect
from werkzeug.security import check_password_hash

from app import db
from app.models.usersmodel import users

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
    return render_template('dashboard/admin/index.html', path=path, route=active_route)


@admin_app_route.route('/admin/reservations/list')
def admin_reservations():
    if not session.get('admin'):
        return redirect('/admin/login')
    path = 'Reservations'
    active_route = request.path
    return render_template('dashboard/admin/reservations.html', path=path, route=active_route)
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
    return render_template('dashboard/admin/bus-list.html', path=path, route=active_route)

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
    return render_template('dashboard/admin/ticket-list.html', path=path,route=active_route)
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
    return render_template('dashboard/admin/route-list.html', path=path, route=active_route)
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
    return render_template('dashboard/admin/users.html', path=path, route=active_route)
@admin_app_route.route('/admin/transactions')
def admin_transactions():
    if not session.get('admin'):
        return redirect('/admin/login')
    path = 'Transactions'
    active_route = request.path
    return render_template('dashboard/admin/transactions.html', path=path, route=active_route)
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
