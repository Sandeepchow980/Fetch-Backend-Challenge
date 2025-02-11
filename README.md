Receipt Points Processor
This project provides a simple REST API built with Flask to process receipts and calculate loyalty points based on various rules. The API allows you to submit receipt data and retrieve calculated points associated with each receipt.

Features
Receipt Processing: Allows users to submit receipt data, which is processed to calculate loyalty points.
Point Calculation: The points are calculated based on several criteria like retailer name, total amount, number of items, item descriptions, and purchase date/time.
Retrieve Points: Users can retrieve the points associated with a specific receipt using a unique receipt ID.
Installation
Clone the Repository:

bash
Copy
Edit
git clone <repository_url>
cd receipt-points-processor
Set up the Virtual Environment:

bash
Copy
Edit
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
Install Dependencies:

bash
Copy
Edit
pip install -r requirements.txt
API Endpoints
POST /receipts/process
Description: Accepts receipt data and processes it to calculate loyalty points.

Request Body: JSON object representing the receipt.

Example:

json
Copy
Edit
{
  "retailer": "SuperMart",
  "total": "25.00",
  "items": [
    {
      "shortDescription": "Bananas",
      "price": "1.50"
    },
    {
      "shortDescription": "Milk",
      "price": "2.00"
    }
  ],
  "purchaseDate": "2025-02-10",
  "purchaseTime": "15:30"
}
Response:

json
Copy
Edit
{
  "id": "unique_receipt_id"
}
GET /receipts/<receipt_id>/points
Description: Retrieves the points for a specific receipt using its unique ID.
Parameters: receipt_id – The unique ID of the receipt.
Response:
json
Copy
Edit
{
  "points": 100
}
Point Calculation Rules
Retailer Name: Add points based on the number of alphanumeric characters in the retailer’s name.
Total Amount: Add 50 points if the total amount is a round dollar (no cents), and 25 points if the total is a multiple of 0.25.
Items Count: Add 5 points for every two items on the receipt.
Item Descriptions: Add points based on the length of the description and item price.
Purchase Date: Add 6 points if the day of the purchase is odd.
Purchase Time: Add 10 points if the purchase time is between 2:00 PM and 4:00 PM.
Running the Application
After setting up the environment, run the Flask application:

bash
Copy
Edit
python app.py
The app will be running on http://127.0.0.1:5000/. You can now interact with the API by sending POST and GET requests to the respective endpoints.
