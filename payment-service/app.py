from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import os

app = Flask(__name__)

# MongoDB configuration
app.config["MONGO_URI"] = os.getenv("MONGO_URI", "mongodb://localhost:27017/paymentdb")
mongo = PyMongo(app)
payments_collection = mongo.db.payments  # Collection to store payment data

# Routes
@app.route('/api/payments', methods=['POST'])
def process_payment():
    data = request.json
    payment_id = payments_collection.insert_one(data).inserted_id
    return jsonify({"payment_id": str(payment_id), "status": "processed"}), 201

@app.route('/api/payments/<payment_id>', methods=['GET'])
def get_payment(payment_id):
    payment = payments_collection.find_one({"_id": ObjectId(payment_id)})
    if payment:
        return jsonify({"amount": payment["amount"], "status": payment["status"]}), 200
    return jsonify({'error': 'Payment not found'}), 404

@app.route('/api/payments/<payment_id>/refund', methods=['PUT'])
def refund_payment(payment_id):
    result = payments_collection.update_one({"_id": ObjectId(payment_id)}, {"$set": {"status": "refunded"}})
    if result.matched_count:
        return jsonify({"message": "Payment refunded"}), 200
    return jsonify({'error': 'Payment not found'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)

