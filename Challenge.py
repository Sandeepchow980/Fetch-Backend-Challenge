from flask import Flask, request, jsonify
import uuid
from datetime import datetime

app = Flask(__name__)

receipt_storage = {}

def compute_points(receipt_data):
    total_points = 0
    
    # Rule 1: Add points based on alphanumeric characters in the retailer name
    total_points += sum(c.isalnum() for c in receipt_data.get("retailer", ""))
    
    # Rule 2: Add 50 points for round dollar amounts (no cents)
    try:
        total_amount = float(receipt_data.get("total", 0))
        if total_amount.is_integer():
            total_points += 50
        
        # Rule 3: Add 25 points if total is divisible by 0.25
        if total_amount % 0.25 == 0:
            total_points += 25
    except ValueError:
        return 0
    
    # Rule 4: Add 5 points for every two items
    item_list = receipt_data.get("items", [])
    total_points += (len(item_list) // 2) * 5
    
    # Rule 5: Add points based on item description length and price
    for item in item_list:
        try:
            description_length = len(item.get("shortDescription", "").strip())
            item_price = float(item.get("price", 0))
            if description_length % 3 == 0:
                total_points += int(item_price * 0.2)
        except ValueError:
            continue
    
    # Rule 6: Add 6 points if the purchase day is odd
    try:
        purchase_date = datetime.strptime(receipt_data.get("purchaseDate", ""), "%Y-%m-%d")
        if purchase_date.day % 2 != 0:
            total_points += 6
    except ValueError:
        return 0
    
    # Rule 7: Add 10 points if purchase time is between 2:00 PM and 4:00 PM
    try:
        purchase_time = datetime.strptime(receipt_data.get("purchaseTime", ""), "%H:%M").time()
        if datetime.strptime("14:00", "%H:%M").time() <= purchase_time <= datetime.strptime("16:00", "%H:%M").time():
            total_points += 10
    except ValueError:
        return 0
    
    return total_points

@app.route("/receipts/process", methods=["POST"])
def process_receipt_data():
    receipt_data = request.get_json()
    if not receipt_data:
        return jsonify({"error": "Invalid JSON format"}), 400
    receipt_id = str(uuid.uuid4())
    receipt_storage[receipt_id] = compute_points(receipt_data)
    return jsonify({"id": receipt_id}), 200

@app.route("/receipts/<receipt_id>/points", methods=["GET"])
def fetch_receipt_points(receipt_id):
    if receipt_id in receipt_storage:
        return jsonify({"points": receipt_storage[receipt_id]}), 200
    return jsonify({"error": "Receipt ID not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)
