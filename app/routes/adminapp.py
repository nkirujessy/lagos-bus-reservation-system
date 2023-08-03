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

@admin_app_route.route('/admin/overview')
def admin_overview():
    if not session.get('admin'):
        return redirect('/admin/login')
    path = 'Control Panel'
    return render_template('dashboard/admin/index.html', path=path)
