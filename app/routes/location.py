from flask import Blueprint, jsonify
from marshmallow import Schema, fields
from app import db, app
from app.models.locationmodel import location
locations_route = Blueprint('locations_route', __name__,template_folder='templates')


class LocationsSchema(Schema):
    class Meta:
        fields = ('id','location','status','created')

location_schema = LocationsSchema()
locations_schema = LocationsSchema(many=True)

@locations_route.route('/locations', methods=['GET'])
def locations():
    locations = db.session.execute(db.select(location).order_by(location.id)).scalars()
    result = locations_schema.dump(locations)
    return jsonify({
        'message': 'Locations Fetched',
        'status': True,
        'data': result

    })
