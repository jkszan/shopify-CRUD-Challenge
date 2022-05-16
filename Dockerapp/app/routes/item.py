from flask import Blueprint, g, request, jsonify, make_response
from app.modules.validation import checkRequiredInput
from app.modules.errors import DatabaseError, InputError
from app.modules.weather import getWeather
from app.modules.query_utils import getProductID, getInventoryID


# This is the largest routes file of this application, it implements the CRUD functionality of items.

# A notable exclusion to this file is some form of endpoint to bulk update items. This is potentially useful to reflect changes when many items are shipped to a different location
# and it can very easily be included in this implementation using the logic of our current update endpoint. You would only need to change the update to use executemany and feed it
# an array of input, either directly or in the form of some 'shipment' or 'batch' table added into the database.


item = Blueprint('item', __name__, url_prefix='/item')

# Route to implement adding items to the database
@item.route('/',
    strict_slashes=False,
    methods=['POST'])
def addItem():

    args = request.args

    serialnumber = args.get("serialnumber", default="", type=int)
    product = args.get("product", default="", type=str)
    condition = args.get("condition", default="New", type=str) # This also defaults to 'New' on the DB side
    damageDescription = args.get("damageDescription", default="", type=str)
    inventory = args.get("inventory", default="", type=str)

    checkRequiredInput({'Serial Number' : serialnumber, 'Product' : product, 'Inventory' : inventory})

    inventoryID = getInventoryID(inventory)
    productID = getProductID(product)

    insertQuery = '''
        INSERT INTO item(serial_number, inventory_id, product_id, condition, damage_description)
        VALUES (%s, %s, %s, %s, %s)'''

    queryValues = [serialnumber, inventoryID, productID, condition, damageDescription]

    try:
        g.dbcursor.execute(insertQuery, queryValues)
        g.dbcon.commit()
    except Exception as e:
        raise DatabaseError(e)

    return make_response("Item added successfully", 201)

# Simple route to get a list of items
@item.route('/',
    strict_slashes=False,
    methods=['GET'])

def getList():
    args = request.args

    serialnumber = args.get("serialnumber", default="", type=int)
    product = args.get("product", default="", type=str)
    inventory = args.get("inventory", default="", type=str)
    condition = args.get("condition", default="", type=str)

    # This query joins all tables in our database to get the full product and address information
    getQuery = '''SELECT serial_number, product_name, product_brand, inventory_name, condition, damage_description, address_city AS city, address_country AS country FROM item NATURAL JOIN product
    NATURAL JOIN inventory NATURAL JOIN address WHERE true'''
    queryValues = []

    if serialnumber:
        getQuery += ' AND serial_number = %s'
        queryValues.append(serialnumber)

    if product:

        if product.isdigit():
            getQuery += ' AND product_id = %s'
        else:
            getQuery += ' AND product_name = %s'

        queryValues.append(product)

    if inventory:

        # If inventory is purely comprised of digits, we assume they are passing ID
        if inventory.isdigit():
            getQuery += ' AND inventory_id = %s'
        else:
            getQuery += ' AND inventory_name = %s'

        queryValues.append(inventory)

    if condition:
        getQuery += ' AND condition = %s'
        queryValues.append(condition)

    try:
        g.dbcursor.execute(getQuery, queryValues)
        items = g.dbcursor.fetchall()
    except Exception as e:
        raise DatabaseError(e)

    # We are rate-limited for how much we can query the OpenWeatherAPI so we get a set of unique cities housing our
    # returned items and get weather information for each instead of calling the API for every item
    citySet = set((item['city'], item['country']) for item in items)
    cityWeather = {}

    for city, country in citySet:
        cityWeather[(city, country)] = getWeather(city, country)

    for item in items:
        item['weather'] = cityWeather[(item['city'], item['country'])]

    return make_response(jsonify(items), 200)

@item.route('/',
    strict_slashes=False,
    methods=['DELETE'])
def deleteItem():

    args = request.args
    serialnumber = args.get("serialnumber", default="", type=int)

    checkRequiredInput({'Serial Number' : serialnumber})

    deleteQuery = 'WITH deletedItems AS (DELETE FROM item WHERE serial_number = %s RETURNING *) SELECT Count(*) as deletecount FROM deletedItems'

    queryValues = [serialnumber]

    try:

        g.dbcursor.execute(deleteQuery, queryValues)
        deletedCount = g.dbcursor.fetchone().get('deletecount')
        g.dbcon.commit()

    except Exception as e:
        raise DatabaseError(e)

    if deletedCount == 0:
        return make_response('No item with specified serial number found', 404)

    return make_response('Item deleted successfully', 200)

@item.route('/',
    strict_slashes=False,
    methods=['PUT'])
def updateItem():

    args = request.args

    product = args.get("product", default="", type=str)
    condition = args.get("condition", default="", type=str)
    damageDescription = args.get("damageDescription", default="", type=str)
    inventory = args.get("inventory", default="", type=str)
    serialnumber = args.get("serialnumber", default="", type=int)

    checkRequiredInput({'Serial Number' : serialnumber})

    if not product and not condition and not damageDescription and not inventory:
        raise InputError("No column update specified")

    updateQuery = 'WITH updatedItems AS (UPDATE item SET serial_number = serial_number'
    queryValues = []

    if product:
        product = getProductID(product)
        updateQuery += ', product_id = %s'
        queryValues.append(product)

    if condition:
        updateQuery += ', condition = %s'
        queryValues.append(condition)

    if damageDescription:
        updateQuery += ', damage_description = %s'
        queryValues.append(damageDescription)

    if inventory:
        inventory = getInventoryID(inventory)
        updateQuery += ', inventory_id = %s'
        queryValues.append(inventory)

    updateQuery += ' WHERE serial_number = %s RETURNING *) SELECT Count(*) as updatecount FROM updatedItems'
    queryValues.append(serialnumber)

    try:
        g.dbcursor.execute(updateQuery, queryValues)
        updateCount = g.dbcursor.fetchone().get('updatecount')
        g.dbcon.commit()
    except Exception as e:
        raise DatabaseError(e)

    if updateCount == 0:
        return make_response('No item with specified serial number found', 404)

    return make_response('Item updated successfully', 200)