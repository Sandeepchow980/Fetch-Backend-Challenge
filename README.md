# Receipt Processor API

This is a Flask-based API that processes receipts and calculates points based on specific rules.

## Installation
1. Clone the repository:
   ```sh
   git clone <repository-url>
   cd <repository-folder>
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Run the application:
   ```sh
   python app.py
   ```

## API Endpoints
### Process a receipt
**POST** `/receipts/process`
- Request Body (JSON):
  ```json
  {
      "retailer": "Walmart",
      "purchaseDate": "2023-05-12",
      "purchaseTime": "14:30",
      "items": [
          {"shortDescription": "Item A", "price": "5.50"},
          {"shortDescription": "Item B", "price": "3.75"}
      ],
      "total": "9.25"
  }
  ```
- Response:
  ```json
  {"id": "<receipt_id>"}
  ```

### Get points for a receipt
**GET** `/receipts/<receipt_id>/points`
- Response:
  ```json
  {"points": 100}
  ```


