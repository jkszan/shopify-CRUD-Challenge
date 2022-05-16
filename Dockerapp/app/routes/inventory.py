from flask import Blueprint, g, make_response, jsonify
from app.modules.errors import DatabaseError


# This file is used to implement inventory management, in a proper implementation we would have a full CRUD system for inventories as well but this is outside the scope
# of the submission. For demo purposes I have manually added in inventories in a script that runs on Docker startup

inventory = Blueprint('inventory', __name__, url_prefix='/inventory')

@inventory.route('/',
    strict_slashes=False,
    methods=['GET'])
def getInventory():

    # Simple query to get relevant information for inventory
    getQuery = 'SELECT inventory_name, owner, size, address_city, address_country, address_state, street_name, house_number, postal_code FROM inventory NATURAL JOIN address'

    try:
        g.dbcursor.execute(getQuery)
        inventories = g.dbcursor.fetchall()
    except Exception as e:
        raise DatabaseError(e)

    # For readability, we will reorganize address information into a subdict
    for inventory in inventories:
        __formatInventory(inventory)

    return make_response(jsonify(inventories), 200)

# Simple helper function to format inventory, could potentially be used in future inventory endpoints
def __formatInventory(inventory):

    inventory['address'] = {
        'City' : inventory.pop('address_city'),
        'Country' : inventory.pop('address_country'),
        'State' : inventory.pop('address_state'),
        'Street Name' : inventory.pop('street_name'),
        'House Number' : inventory.pop('house_number'),
        'Postal Code' : inventory.pop('postal_code')
    }
