from flask import Flask, request, jsonify
import uuid
from datetime import datetime

app = Flask(__name__)

data_store = {}  # Store receipts in memory

def calculate_points(receipt):
    points = 0
    
    # Rule 1: One point for every alphanumeric character in retailer name
    points += sum(c.isalnum() for c in receipt.get("retailer", ""))
    
    # Rule 2: 50 points if total is a round dollar amount with no cents
    try:
        total = float(receipt.get("total", 0))
        if total.is_integer():
            points += 50
        
        # Rule 3: 25 points if total is a multiple of 0.25
        if total % 0.25 == 0:
            points += 25
    except ValueError:
        return 0
    
    # Rule 4: 5 points for every two items on the receipt
    items = receipt.get("items", [])
    points += (len(items) // 2) * 5
    
    # Rule 5: Points based on item descriptions (trimmed length * price)
    for item in items:
        try:
            trimmed_length = len(item.get("shortDescription", "").strip())
            price = float(item.get("price", 0))
            if trimmed_length % 3 == 0:
                points += int(price * 0.2)
        except ValueError:
            continue
    
    # Rule 6: 6 points if the day in purchase date is odd
    try:
        purchase_date = datetime.strptime(receipt.get("purchaseDate", ""), "%Y-%m-%d")
        if purchase_date.day % 2 == 1:
            points += 6
    except ValueError:
        return 0
    
    # Rule 7: 10 points if purchase time is between 2:00 PM and 4:00 PM
    try:
        purchase_time = datetime.strptime(receipt.get("purchaseTime", ""), "%H:%M").time()
        if datetime.strptime("14:00", "%H:%M").time() <= purchase_time <= datetime.strptime("16:00", "%H:%M").time():
            points += 10
    except ValueError:
        return 0
    
    return points

@app.route("/receipts/process", methods=["POST"])
def process_receipt():
    receipt = request.get_json()
    if not receipt:
        return jsonify({"error": "Invalid JSON"}), 400
    receipt_id = str(uuid.uuid4())
    data_store[receipt_id] = calculate_points(receipt)
    return jsonify({"id": receipt_id}), 200

@app.route("/receipts/<receipt_id>/points", methods=["GET"])
def get_points(receipt_id):
    if receipt_id in data_store:
        return jsonify({"points": data_store[receipt_id]}), 200
    return jsonify({"error": "Receipt not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)
