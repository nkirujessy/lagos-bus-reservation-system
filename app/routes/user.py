from flask import request, jsonify, Blueprint, session, redirect
from werkzeug.security import generate_password_hash, check_password_hash

import re
from app.models.usersmodel import users, db
users_route = Blueprint('users_route', __name__,template_folder='templates')

@users_route.route('/signup', methods=['GET', 'POST'])
def register():
    message = ''
    status = False

    if request.method == 'POST' and 'name' in request.form and 'email' in request.form and 'password' in request.form and 'confirmpassword' in request.form:
        fullname = request.form['name']
        email = request.form['email']
        password = request.form['password']
        cpassword = request.form['confirmpassword']
        hashed_password = generate_password_hash(password)
        status = 1
        role = 'user'
        user = users.query.filter_by(email=email).all()


        if cpassword != password:
            message = 'Password doesnt match'
            status = False
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            message = 'Invalid email address !'
            status = False
        elif not password or not email or not fullname:
            message = 'Please fill out the form.'
            status = False
        elif user:
            message = 'User already exists.'
            status = False

        else:
            newuser =  users(fullname=fullname, email=email, password=hashed_password, role=role, status=status)
            db.session.add(newuser)
            db.session.commit()
            message = 'Signup successful'
            status = True
    elif request == 'POST':
        message = 'Please fill out the form !'
        status = False
    return jsonify({
        'message': message,
        'status': status
    })


@users_route.route('/login', methods=['GET', 'POST'])
def login():
    message = ''
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
                message = 'Login successful'
                status = True
        else:
            message = 'Incorrect login details'
            status = False

    return jsonify({
        'message': message,
        'status': status
    })


@users_route.route('/logout')
def logout():
    session.pop('user', None)
    session.pop('id', None)
    session.pop('email', None)
    return redirect('/')
