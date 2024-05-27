#!/usr/bin/python3
"""
Handles all default RESTful API actions for an objects
"""
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields

# Assuming you have a City model defined elsewhere (e.g., models.py)
from models import City, State


class CitySchema(Schema):
  id = fields.Str(dump_only=True)  # Only show id in responses
  name = fields.Str(required=True)
  state_id = fields.Str(required=True)  # Foreign key
  created_at = fields.DateTime(dump_only=True)
  updated_at = fields.DateTime(dump_only=True)

app = Flask(__name__)
db = SQLAlchemy(app)


def get_cities_by_state(state_id):
  state = State.query.get(state_id)
  if not state:
    return jsonify({'error': 'Not found'}), 404
  return jsonify([city.to_dict() for city in state.cities])


def get_city_by_id(city_id):
  city = City.query.get(city_id)
  if not city:
    return jsonify({'error': 'Not found'}), 404
  return jsonify(city.to_dict())


def create_city(state_id):
  data = request.get_json()
  if not data:
    return jsonify({'error': 'Not a JSON'}), 400
  if 'name' not in data:
    return jsonify({'error': 'Missing name'}), 400
  state = State.query.get(state_id)
  if not state:
    return jsonify({'error': 'State not found'}), 404
  new_city = City(name=data['name'], state=state)
  db.session.add(new_city)
  db.session.commit()
  return jsonify(CitySchema().dump(new_city)), 201  # Created


def update_city(city_id):
  data = request.get_json()
  if not data:
    return jsonify({'error': 'Not a JSON'}), 400
  city = City.query.get(city_id)
  if not city:
    return jsonify({'error': 'Not found'}), 404
  for key, value in data.items():
    if key in ['id', 'state_id', 'created_at', 'updated_at']:
      continue  # Ignore these fields
    setattr(city, key, value)
  db.session.commit()
  return jsonify(CitySchema().dump(city))


def delete_city(city_id):
  city = City.query.get(city_id)
  if not city:
    return jsonify({}), 404
  db.session.delete(city)
  db.session.commit()
  return jsonify({})


@app.route('/api/v1/states/<state_id>/cities', methods=['GET'])
def get_cities(state_id):
  return get_cities_by_state(state_id)


@app.route('/api/v1/cities/<city_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_city(city_id):
  if request.method == 'GET':
    return get_city_by_id(city_id)
  elif request.method == 'PUT':
    return update_city(city_id)
  elif request.method == 'DELETE':
    return delete_city(city_id)
  else:
    return jsonify({'error': 'Method not allowed'}), 405
