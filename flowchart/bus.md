op2=>operation: from datetime import datetime, date
op4=>operation: from pprint import pprint
op6=>operation: from flask import Blueprint, request, jsonify, render_template
op8=>operation: from sqlalchemy import between, or_
op10=>operation: from marshmallow import Schema, fields
op12=>operation: from app import db, app
op14=>operation: from app.models.busmodel import bus
op16=>operation: from app.models.ticketmodel import ticket
op18=>operation: from app.models.routemodel import routes
op20=>operation: bus_route = Blueprint('bus_route', __name__, template_folder='templates')
op22=>operation: class ticketSchema(Schema):

    class Meta():
        fields = ('id', 'name', 'description', 'fee', 'routeId', 'busId', 'available', 'availability_date', 'arrival_datetime', 'departure_da
tetime', 'status', 'created')
op24=>operation: ticket_schema = ticketSchema()
op26=>operation: tickets_schema = ticketSchema(many=True)
st29=>start: start buses_search_api
io31=>inputoutput: input:
op34=>operation: message = ''
op36=>operation: status = ''
op38=>operation: data = []
op40=>operation: path = 'Search Result'
cond43=>condition: if (request.method == 'POST')
op47=>operation: start_route = request.form.get('start_route', None)
op49=>operation: end_route = request.form.get('end_route', None)
op51=>operation: dept_date = request.form.get('departure_date', None)
op53=>operation: adult = request.form.get('adult', None)
op55=>operation: children = request.form.get('children', None)
cond58=>condition: if (not start_route)
op62=>operation: message = 'Please select a from destination'
op64=>operation: status = False
io264=>inputoutput: output:  jsonify({'message': message, 'status': status, 'data': data})
e262=>end: end function return
cond69=>condition: if (not end_route)
op73=>operation: message = 'Please select a to destination'
op75=>operation: status = False
cond80=>condition: if (dept_date == '')
op84=>operation: message = 'Please select depature date'
op86=>operation: status = False
cond91=>condition: if (adult == '0')
op95=>operation: message = 'Please add Adult passenger'
op97=>operation: status = False
op101=>operation: check_route = routes.query.filter((routes.start_routeId == start_route), (routes.end_routeId == end_route)).all()
op103=>operation: tickets = []
cond106=>condition: for ro in check_route
op183=>operation: check_date = datetime.strptime(dept_date, '%d/%m/%Y').strftime('%Y-%m-%d')
op185=>operation: tickets = ticket.query.filter(or_((ticket.availability_date >= check_date), (ticket.routeId == ro.id)), (ticket.status == 1
)).all()
cond188=>condition: if tickets
cond193=>condition: for active in tickets
cond223=>condition: if (active.availability_date < date.today())
op227=>operation: message = 'Ticket expired.'
op229=>operation: status = False
op231=>operation: active.status = 0
sub233=>subroutine: db.session.commit()
sub235=>subroutine: continue
op239=>operation: status = True
op241=>operation: message = 'Search result found.'
op243=>operation: data = tickets_schema.dump(tickets)
op250=>operation: status = False
op252=>operation: message = 'No ticket found.'
e270=>end: end buses_search_api
st274=>start: start buses
io276=>inputoutput: input:
op279=>operation: buses = bus.query.all()
op281=>operation: path = 'Buses'
io286=>inputoutput: output:  render_template('/web/busstop.html', result=buses, path=path)
e284=>end: end function return

op2->op4
op4->op6
op6->op8
op8->op10
op10->op12
op12->op14
op14->op16
op16->op18
op18->op20
op20->op22
op22->op24
op24->op26
op26->st29
st29->io31
io31->op34
op34->op36
op36->op38
op38->op40
op40->cond43
cond43(yes)->op47
op47->op49
op49->op51
op51->op53
op53->op55
op55->cond58
cond58(yes)->op62
op62->op64
op64->io264
io264->e262
cond58(no)->cond69
cond69(yes)->op73
op73->op75
op75->io264
cond69(no)->cond80
cond80(yes)->op84
op84->op86
op86->io264
cond80(no)->cond91
cond91(yes)->op95
op95->op97
op97->io264
cond91(no)->op101
op101->op103
op103->cond106
cond106(yes)->op183
op183->op185
op185->cond188
cond188(yes)->cond193
cond193(yes)->cond223
cond223(yes)->op227
op227->op229
op229->op231
op231->sub233
sub233->sub235
cond223(no)->op239
op239->op241
op241->op243
op243->cond193
cond193(no)->cond106
cond188(no)->op250
op250->op252
op252->cond106
cond106(no)->io264
cond43(no)->e270
e270->st274
st274->io276
io276->op279
op279->op281
op281->io286
io286->e284
