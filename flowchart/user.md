op2=>operation: from flask import request, jsonify, Blueprint, session, redirect
op4=>operation: from werkzeug.security import generate_password_hash, check_password_hash
op6=>operation: import re
op8=>operation: from app.helpers.util import generateOTP
op10=>operation: from app.models.usersmodel import users, db
op12=>operation: users_route = Blueprint('users_route', __name__, template_folder='templates')
st15=>start: start register
io17=>inputoutput: input:
op20=>operation: message = ''
op22=>operation: status = False
cond25=>condition: if (request.method == 'POST')
op29=>operation: fullname = request.form['name']
op31=>operation: email = request.form['email']
op33=>operation: password = request.form['password']
op35=>operation: cpassword = request.form['confirmpassword']
op37=>operation: hashed_password = generate_password_hash(password)
op39=>operation: status = 1
op41=>operation: role = ''
cond44=>condition: if (not ('role' in request.form))
op48=>operation: role = 'user'
op55=>operation: user = users.query.filter_by(email=email).all()
cond58=>condition: if (cpassword != password)
op62=>operation: message = 'Password doesnt match'
op64=>operation: status = False
io133=>inputoutput: output:  jsonify({'message': message, 'status': status})
e131=>end: end function return
cond69=>condition: if (not re.match('[^@]+@[^@]+\\.[^@]+', email))
op73=>operation: message = 'Invalid email address !'
op75=>operation: status = False
cond80=>condition: if ((not password) or (not email) or (not fullname))
op84=>operation: message = 'Please fill out the form.'
op86=>operation: status = False
cond91=>condition: if user
op95=>operation: message = 'User already exists.'
op97=>operation: status = False
op101=>operation: newuser = users(fullname=fullname, email=email, password=hashed_password, role=role, code=generateOTP(), status=status)    
sub103=>subroutine: db.session.add(newuser)
sub105=>subroutine: db.session.commit()
op107=>operation: message = 'Signup successful'
op109=>operation: status = True
op52=>operation: role = request.form['role']
cond118=>condition: if (request == 'POST')
op122=>operation: message = 'Please fill out the form !'
op124=>operation: status = False

op2->op4
op4->op6
op6->op8
op8->op10
op10->op12
op12->st15
st15->io17
io17->op20
op20->op22
op22->cond25
cond25(yes)->op29
op29->op31
op31->op33
op33->op35
op35->op37
op37->op39
op39->op41
op41->cond44
cond44(yes)->op48
op48->op55
op55->cond58
cond58(yes)->op62
op62->op64
op64->io133
io133->e131
cond58(no)->cond69
cond69(yes)->op73
op73->op75
op75->io133
cond69(no)->cond80
cond80(yes)->op84
op84->op86
op86->io133
cond80(no)->cond91
cond91(yes)->op95
op95->op97
op97->io133
cond91(no)->op101
op101->sub103
sub103->sub105
sub105->op107
op107->op109
op109->io133
cond44(no)->op52
op52->op55
cond25(no)->cond118
cond118(yes)->op122
op122->op124
op124->io133
cond118(no)->io133
