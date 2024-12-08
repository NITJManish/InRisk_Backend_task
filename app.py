from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Store products in memory
products = []

# Fetch initial data from the Dummy JSON API
def fetch_initial_products():
    global products
    try:
        response = requests.get("https://dummyjson.com/products")
        response.raise_for_status()  # Raise HTTPError for bad responses
        data = response.json()
        products = data.get("products", [])
    except requests.exceptions.RequestException as e:
        products = []
        print(f"Error fetching data from Dummy JSON API: {e}")

# Endpoint to get or add products
@app.route('/products', methods=['GET', 'POST'])
def manage_products():
    if request.method == 'GET':
        # Return the current list of products
        return jsonify(products)

    elif request.method == 'POST':
        # Validate the request body
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON body"}), 400

        required_fields = ["title", "price", "category"]
        missing_fields = [field for field in required_fields if field not in data]

        if missing_fields:
            return jsonify({"error": f"Missing fields: {', '.join(missing_fields)}"}), 400

        # Add the new product to the in-memory list
        new_product = {
            "id": len(products) + 1,  # Generate a simple unique ID
            "title": data["title"],
            "price": data["price"],
            "category": data["category"],
            "description": data.get("description", ""),
            "images": data.get("images", []),
        }
        products.append(new_product)
        return jsonify(products), 201

# Error handling for unexpected routes
@app.errorhandler(404)
def not_found_error(e):
    return jsonify({"error": "Endpoint not found"}), 404

# Error handling for unhandled exceptions
@app.errorhandler(Exception)
def handle_exception(e):
    return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500

if __name__ == '__main__':
    fetch_initial_products()  # Fetch data on application startup
    app.run(debug=True)
