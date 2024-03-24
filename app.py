from pymongo import MongoClient
from flask import Flask, request, jsonify

app = Flask(__name__)                                      # Create an instance of flask

client = MongoClient("localhost", 27017)                   # Database connectivity
database = client['VariantController']                     # Create a new database
collection = database['Variant']                           # Create a new collection in the database



@app.route('/variant', methods=['POST'])                   # Add new products 
def add_variant():
    request_data = request.get_json()
    database.collection.insert_one(request_data)
    new_variant = [{
        'product_id': request_data['product_id'],
        'name': request_data['name'],
        'size': request_data['size'],
        'color': request_data['color'],
        'material': request_data['material']
    }]
    return jsonify(new_variant)


@app.route('/variant/<name>', methods=['GET'])             # Retrive product information along with variants
def get_variant(name):
    query = {
        "name": name
    }
    variants = database.collection.find(query, {'_id': 0, 'product_id': 1, 'name': 1, 'size': 1, 'color': 1, 'material': 1})
    var_list = []
    for v in variants:
        var_list.append(v)
    if not var_list:
        return {
            "message": "Product is not found"
        }, 404
    return {
        "data": var_list
    }, 200


@app.route('/variant/<product_id>', methods=['PUT'])        # Update product information
def update_variant(product_id):
    query = {
        "product_id": product_id
    }
    content = {"$set": dict(request.json)}
    result = database.collection.update_one(query, content)
    if not result.matched_count:
        return {
            "message": "Failed to update. Record is not found"
        }, 404

    if not result.modified_count:
        return {
            "message": "No changes applied"
        }, 500

    return {"message": "Update success"}, 200


@app.route('/variant/<product_id>', methods=['DELETE'])     # Delete product
def delete_variant(product_id):
    query = {
        "product_id": product_id
    }
    result = database.collection.delete_one(query)

    if not result.deleted_count:
        return {
            "message": "Failed to delete"
        }, 500

    return {"message": "Delete success"}, 200


if __name__ == '__main__':
    app.run()
