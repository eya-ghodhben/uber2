from flask import Flask, request, jsonify, render_template
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import os

app = Flask(__name__)

# MongoDB configuration
app.config["MONGO_URI"] = os.getenv("MONGO_URI", "mongodb://localhost:27017/riderdb")
mongo = PyMongo(app)
riders_collection = mongo.db.riders  # Collection to store rider data

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/riders', methods=['POST'])
def create_rider():
    data = request.json
    riders_collection.insert_one(data)
    return jsonify(data), 201

@app.route('/api/riders/<rider_id>', methods=['GET'])
def get_rider(rider_id):
    rider = riders_collection.find_one({"_id": ObjectId(rider_id)})
    if rider:
        return jsonify({"name": rider["name"], "payment_method": rider["payment_method"]}), 200
    return jsonify({'error': 'Rider not found'}), 404

@app.route('/api/riders/<rider_id>', methods=['PUT'])
def update_rider(rider_id):
    data = request.json
    result = riders_collection.update_one({"_id": ObjectId(rider_id)}, {"$set": data})
    if result.matched_count:
        return jsonify(data), 200
    return jsonify({'error': 'Rider not found'}), 404

@app.route('/api/riders/<rider_id>', methods=['DELETE'])
def delete_rider(rider_id):
    result = riders_collection.delete_one({"_id": ObjectId(rider_id)})
    if result.deleted_count:
        return jsonify({'message': 'Rider deleted'}), 204
    return jsonify({'error': 'Rider not found'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)

