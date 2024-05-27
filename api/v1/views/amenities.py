#!/usr/bin/python3
"""
Handles all default RESTful API actions for an objects
"""
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields

# Assuming you have an Amenity model defined elsewhere (e.g., models.py)
from models import Amenity

class AmenitySchema(Schema):
  id = fields.Str(dump_only=True)  # Only show id in responses
  name = fields.Str(required=True)
  created_at = fields.DateTime(dump_only=True)
  updated_at = fields.DateTime(dump_only=True)

app = Flask(__name__)
db = SQLAlchemy(app)

def get_all_amenities():
  amenities = Amenity.query.all()
  return jsonify([amenity.to_dict() for amenity in amenities])

def get_amenity_by_id(amenity_id):
  amenity = Amenity.query.get(amenity_id)
  if not amenity:
    return jsonify({'error': 'Not found'}), 404
  return jsonify(amenity.to_dict())

def create_amenity():
  data = request.get_json()
  if not data:
    return jsonify({'error': 'Not a JSON'}), 400
  if 'name' not in data:
    return jsonify({'error': 'Missing name'}), 400
  new_amenity = Amenity(name=data['name'])
  db.session.add(new_amenity)
  db.session.commit()
  return jsonify(AmenitySchema().dump(new_amenity)), 201  # Created

def update_amenity(amenity_id):
  data = request.get_json()
  if not data:
    return jsonify({'error': 'Not a JSON'}), 400
  amenity = Amenity.query.get(amenity_id)
  if not amenity:
    return jsonify({'error': 'Not found'}), 404
  for key, value in data.items():
    if key in ['id', 'created_at', 'updated_at']:
      continue  # Ignore these fields
    setattr(amenity, key, value)
  db.session.commit()
  return jsonify(AmenitySchema().dump(amenity))

def delete_amenity(amenity_id):
  amenity = Amenity.query.get(amenity_id)
  if not amenity:
    return jsonify({}), 404
  db.session.delete(amenity)
  db.session.commit()
  return jsonify({})

@app.route('/api/v1/amenities/', methods=['GET'])
def get_amenities():
  return get_all_amenities()

@app.route('/api/v1/amenities/<amenity_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_amenity(amenity_id):
  if request.method == 'GET':
    return get_amenity_by_id(amenity_id)
  elif request.method == 'PUT':
    return update_amenity(amenity_id)
  elif request.method == 'DELETE':
    return delete_amenity(amenity_id)
  else:
    return jsonify({'error': 'Method not allowed'}), 405
