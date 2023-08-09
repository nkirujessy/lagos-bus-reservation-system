import json
import random
import string
import sys

from flask import Blueprint, render_template, request, jsonify, session, redirect
from werkzeug.security import check_password_hash

from app import db, app
from app.helpers.util import app_config

from app.models.reservationmodel import reservation
from app.models.routemodel import routes
from app.models.settingsmodel import settings
from app.models.usersmodel import users
from app.models.ticketmodel import ticket
from app.models.busmodel import bus
from app.models.transactionmodel import transaction
from app.models.locationmodel import location
from app.models.busstopmodel import busstop
control_app_route = Blueprint('control_app_route', __name__, template_folder='templates')


def id_generator(size=8, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
@control_app_route.route('/control/login_process', methods=['GET', 'POST'])
def login_process():
    message = 'Error Occurred'
    status = False
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']
        app.logger.info(role)

        if not email:
         message = 'Email is required'
         status=False

        elif not password:
         message = 'Password is required'
         status =False

        else:
             user = users.query.filter_by(email=email).first()
             if user:
                if check_password_hash(user.password, password) and user.role == role:
                    session[role] = True
                    session['id'] = user.id
                    session['email'] = user.email
                    session['fullname'] = user.fullname
                    message = 'Login successful'
                    status = True
    return jsonify({

        'message': message,
        'status': status
    })






@control_app_route.route('/admin/login')
def control_login():
    path = 'Admin Login'
    return render_template('auth/control-login.html', path=path)


@control_app_route.route('/driver/login')
def driver_login():
    path = 'Driver Login'
    return render_template('auth/control-login.html', path=path)
@control_app_route.route('/control/logout')
def control_logout():
    session.pop('admin', None)
    session.pop('id', None)
    session.pop('email', None)
    return redirect('/')
@control_app_route.route('/control/overview')
def control_overview():
    if not session.get('admin') and not session.get('driver'):
        return redirect('/')
    path = 'Control Panel'
    active_route = request.path
    r_count = reservation.query.count()
    route_count = routes.query.count()
    users_count =  users.query.filter_by(role='user').count()
    ticket_count =  ticket.query.count()

    return render_template('dashboard/control/index.html',ticket_count=ticket_count,users_count=users_count, reservation_count=r_count, route_count=route_count,path=path, route=active_route)


@control_app_route.route('/control/reservations/list')
def control_reservations():
    if not session.get('admin') and not session.get('driver'):
        return redirect('/admin/login')
    path = 'Reservations'
    active_route = request.path
    r_list = reservation.query.join(users).all()
    return render_template('dashboard/control/reservation/reservations.html', reserve_list=r_list,path=path, route=active_route)
@control_app_route.route('/control/reservations/search')
def control_reservation_search():
    if not session.get('admin') and not session.get('driver'):
        return redirect('/admin/login')
    path = 'Search Reservation'
    active_route = request.path

    return render_template('dashboard/control/reservation/reservations-search.html', path=path, route=active_route)

@control_app_route.route('/control/reservations/search_process', methods=['POST','GET'])
def control_reservation_search_process():
    if not session.get('admin') and not session.get('driver'):
        return redirect('/admin/login')
    status= False
    message='Error Occurred'
    data=[]

    if request.method == 'POST':
        reserve_number = request.form['reservation_number']

        if not reserve_number:
            message='Reservation number required'
            status=False
        else:
            reservations = reservation.query.filter(reservation.reservation_number==reserve_number).one()
            if reservations:
                status=True

                message='Result found'

                data = reservations.to_dict()
            else:
               message='No result found'
               status=False
    return jsonify({
        'status':status,
        'message':message,
    'data':data
    })

@control_app_route.route('/control/reservations/search/result', methods=['POST','GET'])
def control_reservation_search_result():
    if not session.get('admin') and not session.get('driver'):
        return redirect('/')
    path = 'Reservation Search Result'
    active_route = request.path
    if request.method == 'GET':
        id = request.args.get("id")
        r_details = reservation.query.filter(reservation.id==id).join(users).first()
        if not r_details:
         return redirect('/control/reservations/list')

    return render_template('dashboard/control/reservation/reservations-search-result.html', path=path, route=active_route, result=r_details)
@control_app_route.route('/control/bus/stops')
def control_bus_stops():
    if not session.get('admin'):
        return redirect('/admin/login')
    path = 'Bus Stops'
    active_route = request.path
    b_list = busstop.query.join(routes).all()

    return render_template('dashboard/control/bus/bus-stop-list.html',bus_list=b_list,path=path, route=active_route)
@control_app_route.route('/control/bus/list')
def control_bus_list():
    if not session.get('admin'):
        return redirect('/admin/login')
    path = 'Bus List'
    active_route = request.path
    b_list = bus.query.join(users).all()

    return render_template('dashboard/control/bus/bus-list.html',bus_list=b_list,path=path, route=active_route)

@control_app_route.route('/control/bus/add')
def control_bus_add():
    if not session.get('admin'):
        return redirect('/admin/login')
    path = 'Add Bus'
    active_route = request.path
    dr_list = users.query.filter(users.role=='driver').all()
    return render_template('dashboard/control/bus/bus-add.html', drivers_list=dr_list, path=path, route=active_route)

@control_app_route.route('/control/bus/edit',methods=['GET','POST'])
def control_bus_edit():
 if not session.get('admin'):
    return redirect('/admin/login')
 if request.method == 'GET':
     path = 'Edit Bus'
     active_route = request.path
     dr_list = users.query.filter(users.role=='driver').all()
     id = request.args.get('id')
     result = bus.query.filter(bus.id==id).first()
     if not result:
       return redirect('/control/bus/list')

 return render_template('dashboard/control/bus/bus-edit.html', result=result, drivers_list=dr_list, path=path, route=active_route)
@control_app_route.route('/control/bus/edit_process', methods=['POST','GET'])
def control_bus_edit_process():
    status = False
    message = 'Error Occurred'
    if not session.get('admin'):
        return redirect('/admin/login')
    if request.method == 'POST':
        id = request.form['id']
        name = request.form['name']
        occupancy = request.form['occupancy']
        driver = request.form['driver']
        stat = request.form['status']
        desc = request.form['description']
        adult = request.form['adult']
        children = request.form['children']
        stat = request.form['status']

        if not name:
            message = 'Bus name is required'
            status= False
        elif not occupancy:
            message = 'Occupancy is required'
            status = False
        elif not driver:
            message = 'Driver is required'
            status = False
        elif not adult:
            message = 'Adult is required'
            status = False
        elif not children:
            message = 'Children is required'
            status = False
        elif not desc:
            message = 'Description is required'
            status = False
        elif not stat:
            message = 'Status is required'
            status = False


        else:
            data = bus.query.filter(bus.id==id).first()
            data.name=name
            data.driverId=driver
            data.max_occupancy=occupancy
            data.description=desc
            data.adult=adult
            data.children=children
            data.status=stat

            db.session.commit()
            status = True
            message = 'Bus updated.'

    return jsonify({
        'message': message,
        'status': status
    })
@control_app_route.route('/control/bus/stop/add')
def control_bus_stop_add():
    if not session.get('admin'):
        return redirect('/admin/login')
    path = 'Add Bus Stop'
    active_route = request.path
    r_list = routes.query.all()
    return render_template('dashboard/control/bus/bus-stop-add.html', routes_list=r_list, path=path, route=active_route)
@control_app_route.route('/control/bus/stop/edit')
def control_bus_stop_edit():
    if not session.get('admin'):
        return redirect('/admin/login')
    path = 'Edit Bus Stop'
    active_route = request.path
    r_list = routes.query.all()
    if request.method == 'GET':
     id = request.args.get('id')
     result = busstop.query.filter(busstop.id==id).first()
     if not result:
        return redirect('/control/bus/list')

    return render_template('dashboard/control/bus/bus-stop-edit.html', result=result, routes_list=r_list, path=path, route=active_route)
@control_app_route.route('/control/bus/stop/edit_process', methods=['POST','GET'])
def control_bus_stop_edit_process():
    status = False
    message = 'Error Occurred'
    if not session.get('admin'):
        return redirect('/admin/login')
    if request.method == 'POST':
        id = request.form['id']
        name = request.form['name']
        route = request.form['route']
        address = request.form['address']
        landmark = request.form['landmark']
        zip = request.form['zip']
        stat = request.form['status']
        desc = request.form['description']
        long = request.form['longitude']
        lat = request.form['latitude']
        stat = request.form['status']

        if not name:
            message = 'Bus name is required'
            status= False
        elif not route:
            message = 'Route is required'
            status = False
        elif not address:
            message = 'Address is required'
            status = False
        elif not landmark:
            message = 'Landmark is required'
            status = False
        elif not zip:
            message = 'Zip is required'
            status = False
        elif not desc:
            message = 'Description is required'
            status = False
        elif not stat:
            message = 'Status is required'
            status = False
        elif not long:
            message = 'Longitude is required'
            status = False
        elif not lat:
            message = 'Latitude is required'
            status = False


        else:
            data = busstop.query.filter(busstop.id==id).first()
            data.name=name
            data.routeId=route
            data.address=address
            data.description=desc
            data.landmark=landmark
            data.zipcode=zip
            data.latitude=lat
            data.longitude=long
            data.status=stat

            db.session.commit()
            status = True
            message = 'Bus Stop updated.'

    return jsonify({
        'message': message,
        'status': status
    })
@control_app_route.route('/control/bus/stop/add_process', methods=['POST','GET'])
def control_bus_stop_add_process():
    status = False
    message = 'Error Occurred'
    if not session.get('admin'):
        return redirect('/admin/login')
    if request.method == 'POST':
        name = request.form['name']
        route = request.form['route']
        lat = request.form['latitude']
        long = request.form['longitude']
        address = request.form['address']
        zip = request.form['zip']
        landmark = request.form['landmark']
        desc = request.form['description']
        status = 1
        check_name = busstop.query.filter_by(name=name).first()

        if check_name:
            message = 'Bus Stop with name already exist.'
            status= False
        if not name:
            message = 'Bus Stop name is required'
            status= False
        elif not route:
            message = 'Route is required'
            status = False
        elif not lat:
            message = 'Latitude is required'
            status = False
        elif not long:
            message = 'Longitude is required'
            status = False
        elif not address:
            message = 'Address is required'
            status = False
        elif not zip:
            message = 'Zip is required'
            status = False
        elif not landmark:
            message = 'Landmark is required'
            status = False
        elif not desc:
            message = 'Description is required'
            status = False

        else:
            newstop =  busstop(name=name,latitude=lat,landmark=landmark, longitude=long, address=address,zipcode=zip,description=desc,routeId=route,  status=status)
            db.session.add(newstop)
            db.session.commit()
            status = True
            message = 'Bus Stop created.'
    elif request == 'POST':
        message = 'Please fill out the form !'

    return jsonify({
        'message': message,
        'status': status
    })
@control_app_route.route('/control/bus/add_process', methods=['POST','GET'])
def control_bus_add_process():
    status = False
    message = 'Error Occurred'
    if not session.get('admin'):
        return redirect('/admin/login')
    if request.method == 'POST':
        bus_name = request.form['bus_name']
        capacity = request.form['max_occupancy']
        adult = request.form['adult']
        children = request.form['children']
        driver = request.form['driver']
        desc = request.form['description']
        status = 1
        check_name = bus.query.filter_by(name=bus_name).first()

        if check_name:
            message = 'Bus with number already exist.'
            status= False
        if not bus_name:
            message = 'Bus number is required'
            status= False
        elif not capacity:
            message = 'Maximum occupancy is required'
            status = False
        elif not driver:
            message = 'Driver is required'
            status = False
        elif not adult:
            message = 'Adult is required'
            status = False
        elif not children:
            message = 'Children is required'
            status = False
        elif not desc:
            message = 'Description is required'
            status = False

        else:
            newbus =  bus(name=bus_name,description=desc,max_occupancy=capacity, adult=adult, children=children,driverId=driver,  status=status)
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

@control_app_route.route('/control/ticket/list')
def control_ticket_list():
    if not session.get('admin'):
        return redirect('/admin/login')
    path = 'Ticket List'
    active_route = request.path
    # t_list = ticket.query.all()
    t_list = ticket.query.join(users).join(bus).join(routes).all()
    currency=app_config().currency

    return render_template('dashboard/control/ticket/ticket-list.html',ticket_list=t_list, path=path,route=active_route, currency=currency)
@control_app_route.route('/control/ticket/add')
def control_ticket_add():
    if not session.get('admin'):
        return redirect('/admin/login')
    path = 'Ticket Add'
    active_route = request.path
    routes_list = routes.query.filter_by(status=1).all()
    bus_list = bus.query.filter_by(status=1).all()
    dr_list = users.query.filter(users.role=='driver').all()
    return render_template('dashboard/control/ticket/ticket-add.html',drivers_list=dr_list, bus_list=bus_list,routes_list=routes_list, path=path, route=active_route)

@control_app_route.route('/control/ticket/edit', methods=['POST','GET'])
def control_ticket_details():
    if not session.get('admin'):
        return redirect('/admin/login')
    path = 'Edit Ticket'
    active_route = request.path
    if request.method == 'GET':
     id = request.args.get('id')
    routes_list = routes.query.filter_by(status=1).all()
    bus_list = bus.query.filter_by(status=1).all()
    dr_list = users.query.filter(users.role=='driver').all()
    t_list = ticket.query.filter(ticket.id==id).join(users).join(bus).join(routes).first()

    if not t_list:
        return redirect('/control/ticket/list')

    return render_template('dashboard/control/ticket/ticket-edit.html',drivers_list=dr_list, bus_list=bus_list,routes_list=routes_list, result=t_list, path=path, route=active_route)
@control_app_route.route('/control/ticket/add_process', methods=['POST','GET'])
def control_ticket_add_process():
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
        driver = request.form['driver']
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
        elif not driver:
            message = 'Driver is required'
            status = False
        elif not route:
            message = 'Route is required'
            status = False
        elif not desc:
            message = 'Description is required'
            status = False


        else:
            data =  ticket(name=name,description=desc,fee=fee, ticket_number=ticket_number, routeId=route,busId=bus,available=available, availability_date=avail_date, arrival_datetime=arrival,departure_datetime=dept, driverId=driver, status=status)
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

@control_app_route.route('/control/ticket/edit_process', methods=['POST','GET'])
def control_ticket_edit_process():
    status = False
    message = 'Error Occurred'
    if not session.get('admin'):
        return redirect('/admin/login')
    if request.method == 'POST':
        id = request.form['id']
        name = request.form['name']
        fee = request.form['fee']
        available = request.form['available']
        avail_date = request.form['availability_date']
        dept = request.form['departure_time']
        arrival = request.form['arrival_time']
        bus = request.form['bus']
        driver = request.form['driver']
        route = request.form['route']
        desc = request.form['description']
        stat = request.form['status']

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
        elif not driver:
            message = 'Driver is required'
            status = False
        elif not route:
            message = 'Route is required'
            status = False
        elif not desc:
            message = 'Description is required'
            status = False
        elif not stat:
            message = 'Status is required'
            status = False


        else:
            data = ticket.query.filter(ticket.id==id).first()
            data.name=name
            data.fee=fee
            data.available=available
            data.availability_date=avail_date
            data.departure_datetime=dept
            data.arrival_datetime=arrival
            data.busId= bus
            data.driverId=driver
            data.routeId=route
            data.description=desc
            data.status=stat

            db.session.commit()
            status = True
            message = 'Ticket created.'

    return jsonify({
        'message': message,
        'status': status
    })

@control_app_route.route('/control/routes/list')
def control_routes_list():
    if not session.get('admin'):
        return redirect('/admin/login')
    path = 'Routes List'
    active_route = request.path
    r_list = routes.query.all()
    app.logger.info(r_list)
    return render_template('dashboard/control/route/route-list.html' ,route_list=r_list, path=path, route=active_route)

@control_app_route.route('/control/routes/edit')
def control_routes_edit():
    if not session.get('admin'):
        return redirect('/admin/login')
    path = 'Routes Edit'
    active_route = request.path
    id = request.args.get('id')
    r_list = routes.query.filter(routes.id==id).first()

    locations = location.query.all()
    if not r_list:
       return redirect('/control/routes/list')

    return render_template('dashboard/control/route/route-edit.html' ,result=r_list, locations=locations,path=path, route=active_route)
@control_app_route.route('/control/routes/edit_process', methods=['POST','GET'])
def control_route_edit_process():
    status = False
    message = 'Error Occurred'
    if not session.get('admin'):
        return redirect('/admin/login')
    if request.method == 'POST':
        id = request.form['id']
        name = request.form['name']
        start = request.form['start_route']
        end = request.form['end_route']
        desc = request.form['description']
        stat = request.form['status']

        if not name:
            message = 'Route name is required'
            status= False
        elif not start:
            message = 'Start route is required'
            status = False
        elif not end:
            message = 'End route is required'
            status = False
        elif not desc:
            message = 'Description is required'
            status = False
        elif not stat:
            message = 'Status is required'
            status = False


        else:
            data = routes.query.filter(routes.id==id).first()
            data.name=name
            data.start_routeId=start
            data.end_routeId=end
            data.description=desc
            data.status=stat

            db.session.commit()
            status = True
            message = 'Route updated.'

    return jsonify({
        'message': message,
        'status': status
    })
@control_app_route.route('/control/routes/add')
def control_routes_add():
    if not session.get('admin'):
        return redirect('/admin/login')
    path = 'Add Route'
    active_route = request.path
    locations = location.query.all()
    return render_template('dashboard/control/route/route-add.html', locations=locations,path=path, route=active_route)
@control_app_route.route('/control/route/add_process', methods=['POST','GET'])
def control_route_add_process():
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
@control_app_route.route('/control/users')
def control_users():
    if not session.get('admin'):
        return redirect('/admin/login')
    path = 'Users'
    active_route = request.path
    u_list =  users.query.all()
    return render_template('dashboard/control/user/users.html', users_list=u_list, path=path, route=active_route)
@control_app_route.route('/control/transactions')
def control_transactions():
    if not session.get('admin'):
        return redirect('/admin/login')
    path = 'Transactions'
    active_route = request.path
    t_list = transaction.query.all()
    return render_template('dashboard/control/transactions.html',transaction_list=t_list, path=path, route=active_route)
@control_app_route.route('/control/settings', methods=['POST','GET' ])
def control_settings():
    if not session.get('admin'):
        return redirect('/admin/login')
    path = 'Settings'
    active_route = request.path
    config = app_config()
    if request.method == 'POST':
        id = request.form['id']
        name = request.form['appname']
        curr = request.form['currency']
        email = request.form['email']
        password = request.form['password']
        host = request.form['host']
        port = request.form['port']
        setting = settings.query.filter(settings.id==id).first()
        setting.appname=name
        setting.currency=curr
        setting.email=email
        setting.password=password
        setting.host=host
        setting.port=port
        db.session.commit()
        if setting:
         return redirect('/control/settings')

    return render_template('dashboard/control/settings.html', config=config,path=path, route=active_route)
@control_app_route.route('/control/profile')
def control_profile():
    if not session.get('admin') and not session.get('driver'):
        return redirect('/')
    path = 'Profile'
    active_route = request.path
    user = users.query.filter(users.id==session.get('id')).first()
    return render_template('dashboard/control/profile.html', path=path, route=active_route, user=user)

@control_app_route.route('/control/user/delete', methods=['GET'])
def control_user_delete():
    if not session.get('admin') :
        return redirect('/')
    message='Error Occurred'
    status= False
    if request.method == 'GET':
        id = request.args.get('id')

        user = users.query.filter(users.id==id).first()

        if not user:
            message='User not found'
            status= False
        else:
            db.session.delete(user)
            db.session.commit()
            message='User Deleted'
            status= True

    return jsonify({
        'message':message,
        'status':status,
    })


@control_app_route.route('/control/ticket/delete', methods=['GET'])
def control_ticket_delete():
    if not session.get('admin') :
        return redirect('/')
    message='Error Occurred'
    status= False
    if request.method == 'GET':
        id = request.args.get('id')

        data = ticket.query.filter(ticket.id==id).first()

        if not data:
            message='Ticket not found'
            status= False
        else:
            db.session.delete(data)
            db.session.commit()
            message='Ticket Deleted'
            status= True

    return jsonify({
        'message':message,
        'status':status,
    })
# Driver


@control_app_route.route('/control/driver/bus/list')
def control_driver_bus_list():
    if not  session.get('driver'):
        return redirect('/driver/login')
    path = 'My Bus'
    active_route = request.path
    user = session.get('id')
    b_list = bus.query.filter(bus.driverId==user).join(users).all()

    return render_template('dashboard/control/bus/driver-bus-list.html',bus_list=b_list,path=path, route=active_route)

@control_app_route.route('/control/trips/list')
def control_driver_trips_list():
    if not session.get('driver'):
        return redirect('/driver/login')
    path = 'My Trips'
    active_route = request.path
    user = session.get('id')
    t_list = ticket.query.filter(ticket.driverId==user).join(users).all()

    return render_template('dashboard/control/reservation/driver-trip-list.html',trip_list=t_list,path=path, route=active_route)
