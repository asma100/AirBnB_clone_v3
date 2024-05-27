#!/usr/bin/python3
"""
App views for AirBnB_clone_v3
"""

from flask import jsonify
from models import storage
from api.v1.views import app_views
from models import storage
from models.base_model import BaseModel
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route('/status')
def status():
    """ returns status """
    status = {"status": "OK"}
    return jsonify(status)


@app_views.route('/stats')
def get_stats():
    """ Returns the number of objects of each type. """
    classes = {
        "Amenity": storage.count(Amenity),
        "City": storage.count(City),
        "Place": storage.count(Place),
        "Review": storage.count(Review),
        "State": storage.count(State),
        "User": storage.count(User),
    }
    return jsonify(classes)
