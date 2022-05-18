from flask import Blueprint, g, make_response, jsonify, request
from app.modules.errors import DatabaseError
from app.modules.validation import checkRequiredInput


# This file is used to implement inventory management, in a proper implementation we would have a full CRUD system for inventories

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

@inventory.route('/',
    strict_slashes=False,
    methods=['POST'])
def addInventory():

    args = request.args
    address_id = args.get("address_id", default="", type=int)
    inventory_name = args.get("name", default="", type=str)
    owner = args.get("name", default="", type=str)

    checkRequiredInput({"Address": address_id, "Name": inventory_name})

    insertQuery = 'INSERT INTO inventory(address_id, inventory_name, owner) VALUES (%s, %s, %s)'

    queryValues = [address_id, inventory_name, owner]

    try:
        g.dbcursor.execute(insertQuery, queryValues)
        g.dbcon.commit()
    except Exception as e:
        raise DatabaseError(e)

    return make_response("Inventory added successfully", 201)

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
