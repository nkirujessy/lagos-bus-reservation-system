from flask import request, jsonify, Blueprint, session, redirect
from werkzeug.security import generate_password_hash, check_password_hash

import re

from app.helpers.util import generateOTP
from app.models.usersmodel import users, db

users_route = Blueprint('users_route', __name__, template_folder='templates')

def test():



@users_route.route('/signup', methods=['GET', 'POST'])
def register():
    message = ''
    status = False

    if request.method == 'POST':
        fullname = request.form['name']
        email = request.form['email']
        password = request.form['password']
        cpassword = request.form['confirmpassword']
        hashed_password = generate_password_hash(password)
        status = 1
        role = ''
        if not 'role' in request.form:
            role = 'user'
        else:
            role = request.form['role']

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
            newuser = users(fullname=fullname, email=email, password=hashed_password, role=role, code=generateOTP(), status=status)
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
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = db.one_or_404(db.select(users).filter_by(email=email))

        if user:
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


@users_route.route('/profile/password/update', methods=['GET', 'POST'])
def profile_update_password():
    try:
        user = session.get('id')
        status = False
        message = 'Error Occurred'
        if not user:
            redirect('/')
        if request.method == 'POST':
                oldpassword = request.form['oldpassword']
                newpassword = request.form['newpassword']
                confirmpassword = request.form['confirmpassword']
                hashed_password = generate_password_hash(newpassword)
                profile = users.query.filter(users.id == user).first()
                if not profile:
                    status = False
                    message = 'Unauthorized. Please refresh page.'
                elif not oldpassword:
                    status = False
                    message = 'Old password is required.'
                elif not newpassword:
                    status = False
                    message = 'New password is required.'
                elif not oldpassword:
                    status = False
                    message = 'Confirm password is required.'
                elif not check_password_hash(profile.password, oldpassword):
                    status = False
                    message = 'Old password is incorrect.'
                elif confirmpassword != newpassword:
                    status = False
                    message = 'Password mismatch. Confirm password must match new password.'
                else:
                    profile.password = hashed_password
                    db.session.commit()
                    status = True
                    message = 'Password updated.'

        return jsonify({
                'status': status,
                'message': message
            })

    except NameError:
        raise Exception(NameError)
@users_route.route('/logout')
def logout():
    session.pop('user', None)
    session.pop('id', None)
    session.pop('email', None)
    return redirect('/')


@users_route.route('/password/reset/request', methods=['POST', 'GET'])
def reset_password():
    status = False
    message = 'Error Occurred'
    if request.method == 'POST':
        email = request.form['email']
        user = users.query.filter(users.email==email).first()
        if not user:
            status = False
            message = 'User not found.'
        else:
           status = True
           message = 'Password reset code sent to email.'

    return jsonify({
        'status': status,
        'message': message
    })
@users_route.route('/profile/update', methods=['POST', 'GET'])
def profile_update():
        user = session.get('id')
        status = False
        message = 'Error Occurred'
        if not user:
            redirect('/')
        if request.method == 'POST':
            name = request.form.get('fullname', None)
            email = request.form.get('email', None)
            profile = users.query.filter(users.id == user).first()
            if not profile:
               status = False
               message = 'Unauthorized. Please refresh page.'
            else:
              profile.fullname = name
              profile.email = email
              db.session.commit()
              status = True
              message = 'Profile updated.'

        return jsonify({
            'status': status,
            'message': message
        })

