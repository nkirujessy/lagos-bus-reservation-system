from flask import request, jsonify, Blueprint, session, redirect
from werkzeug.security import generate_password_hash, check_password_hash

import re
from app.models.usersmodel import users, db
users_route = Blueprint('users_route', __name__,template_folder='templates')

@users_route.route('/signup', methods=['GET', 'POST'])
def register():
    msg = ''
    status = False

    if request.method == 'POST' and 'name' in request.form and 'email' in request.form and 'password' in request.form and 'confirmpassword' in request.form:
        fullname = request.form['name']
        email = request.form['email']
        password = request.form['password']
        cpassword = request.form['confirmpassword']
        hashed_password = generate_password_hash(password)
        status = 1
        role = 'user'
        user = db.session.execute(db.select(users).filter_by(email=email)).scalar_one()


        if cpassword != password:
            msg = 'Password doesnt match'
        elif user:
            msg = 'User already exists.'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not password or not email or not fullname:
            msg = 'Please fill out the form.'

        else:
            newuser =  users(fullname=fullname, email=email, password=hashed_password, role=role, status=status)
            db.session.add(newuser)
            db.session.commit()
            status = True
            msg = 'Signup successful'
    elif request == 'POST':
        msg = 'Please fill out the form !'
    return jsonify({
        'message': msg,
        'user': status
    })


@users_route.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    status = False
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']

        user = db.one_or_404(db.select(users).filter_by(email=email))


        if user :
            if check_password_hash(user.password, password) and user.role == "user":
                session['user'] = True
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


@users_route.route('/logout')
def logout():
    session.pop('user', None)
    session.pop('id', None)
    session.pop('email', None)
    return redirect('/')
