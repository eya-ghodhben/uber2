from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import os

app = Flask(__name__)

# MongoDB configuration
app.config["MONGO_URI"] = os.getenv("MONGO_URI", "mongodb://localhost:27017/ridedb")
mongo = PyMongo(app)
rides_collection = mongo.db.rides  # Collection to store ride data

# Routes
@app.route('/api/rides', methods=['POST'])
def create_ride():
    data = request.json
    data['status'] = 'pending'
    ride_id = rides_collection.insert_one(data).inserted_id
    return jsonify({"ride_id": str(ride_id), "status": data['status']}), 201

@app.route('/api/rides/<ride_id>', methods=['GET'])
def get_ride(ride_id):
    ride = rides_collection.find_one({"_id": ObjectId(ride_id)})
    if ride:
        return jsonify({"status": ride["status"], "driver_id": ride.get("driver_id")}), 200
    return jsonify({'error': 'Ride not found'}), 404

@app.route('/api/rides/<ride_id>/assign_driver', methods=['PUT'])
def assign_driver(ride_id):
    data = request.json
    result = rides_collection.update_one({"_id": ObjectId(ride_id)}, {"$set": {"driver_id": data["driver_id"], "status": "assigned"}})
    if result.matched_count:
        return jsonify({"message": "Driver assigned", "status": "assigned"}), 200
    return jsonify({'error': 'Ride not found'}), 404

@app.route('/api/rides/<ride_id>/complete', methods=['PUT'])
def complete_ride(ride_id):
    result = rides_collection.update_one({"_id": ObjectId(ride_id)}, {"$set": {"status": "completed"}})
    if result.matched_count:
        return jsonify({"message": "Ride completed"}), 200
    return jsonify({'error': 'Ride not found'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)

