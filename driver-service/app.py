from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_pymongo import PyMongo
from bson.objectid import ObjectId  # Ajout de l'import ObjectId
import os

app = Flask(__name__)

# MongoDB configuration
app.config["MONGO_URI"] = os.getenv("MONGO_URI", "mongodb://localhost:27017/driverdb")
mongo = PyMongo(app)
drivers_collection = mongo.db.drivers  # Collection to store driver data

# Route par défaut
@app.route('/')
def home():
    return redirect(url_for('show_drivers'))

# Routes
@app.route('/drivers', methods=['GET'])
def show_drivers():
    drivers = drivers_collection.find()
    return render_template('show-drivers.html', drivers=drivers)  # Assurez-vous que le nom du fichier est correct

@app.route('/add-driver', methods=['GET', 'POST'])
def add_driver():
    if request.method == 'POST':
        name = request.form.get('name')
        license = request.form.get('license')
        available = 'available' in request.form
        drivers_collection.insert_one({
            'name': name,
            'license': license,
            'available': available
        })
        return redirect(url_for('show_drivers'))  # Cette route doit correspondre à '/drivers'
    return render_template('add-driver.html')  # Assurez-vous que le nom du fichier est correct

@app.route('/api/drivers', methods=['POST'])
def create_driver():
    data = request.json
    drivers_collection.insert_one(data)
    return jsonify(data), 201

@app.route('/api/drivers/<driver_id>', methods=['GET'])
def get_driver(driver_id):
    driver = drivers_collection.find_one({"_id": ObjectId(driver_id)})
    if driver:
        return jsonify({"name": driver["name"], "license": driver["license"], "available": driver["available"]}), 200
    return jsonify({'error': 'Driver not found'}), 404

@app.route('/api/drivers/<driver_id>', methods=['PUT'])
def update_driver(driver_id):
    data = request.json
    result = drivers_collection.update_one({"_id": ObjectId(driver_id)}, {"$set": data})
    if result.matched_count:
        return jsonify(data), 200
    return jsonify({'error': 'Driver not found'}), 404

@app.route('/api/drivers/<driver_id>', methods=['DELETE'])
def delete_driver(driver_id):
    result = drivers_collection.delete_one({"_id": ObjectId(driver_id)})
    if result.deleted_count:
        return jsonify({'message': 'Driver deleted'}), 204
    return jsonify({'error': 'Driver not found'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)

