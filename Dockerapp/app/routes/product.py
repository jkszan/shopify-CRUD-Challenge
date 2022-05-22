from flask import Blueprint, g, make_response, jsonify
from app.modules.errors import DatabaseError


# This file is used to implement product management. Much like in the inventory.py, a proper implementation would have a full CRUD system for product but this is outside the scope
# of this submission. For demo purposes I have manually added products in through a script that runs on Docker startup

product = Blueprint('product', __name__, url_prefix='/product')

# Simple endpoint to grab product information for demo
@product.route('/',
    methods=['GET'])
def getProduct():

    getQuery = 'SELECT product_name, product_brand, product_description FROM product'

    try:
        g.dbcursor.execute(getQuery)
        products = g.dbcursor.fetchall()
    except Exception as e:
        raise DatabaseError(e)

    return make_response(jsonify(products), 200)
