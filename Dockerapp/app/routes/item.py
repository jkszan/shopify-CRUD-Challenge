from flask import Blueprint, g, request, jsonify, make_response
from os import environ
from app.routes import requires
from app.modules.errors import InputError
from app.modules.weather import getWeather
from app.modules.query_utils import getProductID, getInventoryID


# This is the largest routes file of this application, it implements all of the CRUD functionality for items.

item = Blueprint('item', __name__, url_prefix='/item')

# Route to implement adding items to the database
@item.route('/',
    methods=['POST'])
@requires('serialnumber', 'product', 'inventory')
def addItem():

    args = request.args

    serialnumber = args.get("serialnumber", type=int)
    product = args.get("product", type=str)
    condition = args.get("condition", default="New", type=str) # This also defaults to 'New' on the DB side
    damageDescription = args.get("damageDescription", type=str)
    inventory = args.get("inventory", type=str)

    inventoryID = getInventoryID(inventory)
    productID = getProductID(product)

    insertQuery = '''
        INSERT INTO item(serial_number, inventory_id, product_id, condition, damage_description)
        VALUES (%s, %s, %s, %s, %s)'''

    queryValues = [serialnumber, inventoryID, productID, condition, damageDescription]

    g.dbcursor.execute(insertQuery, queryValues)
    g.dbcon.commit()

    return make_response("Item added successfully", 201)

# Simple route to get a list of items
@item.route('/',
    methods=['GET'])

def getList():
    args = request.args

    serialnumber = args.get("serialnumber", type=int)
    product = args.get("product", type=str)
    inventory = args.get("inventory", type=str)
    condition = args.get("condition", type=str)

    # This query joins all tables in our database to get the full product and address information
    getQuery = '''SELECT serial_number, product_name, product_brand, inventory_name, condition, damage_description, address_city AS city, address_country AS country FROM item NATURAL JOIN product
    NATURAL JOIN inventory NATURAL JOIN address WHERE true'''
    queryValues = []

    if serialnumber:
        getQuery += ' AND serial_number = %s'
        queryValues.append(serialnumber)

    # While we can easily translate a product or inventory name to ID, we have both values in the returned dataset so there is no
    # reason to make the additional queries
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

    g.dbcursor.execute(getQuery, queryValues)
    items = g.dbcursor.fetchall()

    # Getting weather information and adding it to a value in our dictionary
    __getWeatherInformation(items)

    return make_response(jsonify(items), 200)

def __getWeatherInformation(items):

    # Checking if there is an entry defined for WEATHER_APIKEY
    if not "WEATHER_APIKEY" in environ:
        g.appLogger.error('OpenWeatherAPI env variable does not exist, cannot get weather information')
        return

    # Checking if the entry for WEATHER_APIKEY is instantiated
    if not environ['WEATHER_APIKEY']:
        g.appLogger.error('No OpenWeatherAPI key set, cannot get weather information')
        return


    # We are rate-limited for how much we can query the OpenWeatherAPI so we get a set of unique cities housing our
    # returned items and get weather information for each instead of calling the API for every item
    citySet = set((item['city'], item['country']) for item in items)
    cityWeather = {}

    for city, country in citySet:

        # Catching any errors from the weather collection script
        try:
            cityWeather[(city, country)] = getWeather(city, country)
        except Exception as e:
            g.appLogger.error("Error encountered when finding weather: \n" + str(e))
            cityWeather[(city, country)] = 'Unknown, error encountered'

    for item in items:
        item['weather'] = cityWeather[(item['city'], item['country'])]

@item.route('/',
    methods=['DELETE'])
@requires('serialnumber')
def deleteItem():

    args = request.args
    serialnumber = args.get("serialnumber", type=int)

    deleteQuery = 'WITH deletedItems AS (DELETE FROM item WHERE serial_number = %s RETURNING *) SELECT Count(*) as deletecount FROM deletedItems'

    queryValues = [serialnumber]

    g.dbcursor.execute(deleteQuery, queryValues)
    deletedCount = g.dbcursor.fetchone().get('deletecount')
    g.dbcon.commit()

    if deletedCount == 0:
        return make_response('No item with specified serial number found', 404)

    return make_response('Item deleted successfully', 200)

@item.route('/',
    methods=['PUT'])
@requires('serialnumber')
def updateItem():

    args = request.args

    product = args.get("product", type=str)
    condition = args.get("condition", type=str)
    damageDescription = args.get("damage_description", type=str)
    inventory = args.get("inventory", type=str)
    serialnumber = args.get("serialnumber", type=int)

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

    g.dbcursor.execute(updateQuery, queryValues)
    updateCount = g.dbcursor.fetchone().get('updatecount')
    g.dbcon.commit()


    if updateCount == 0:
        return make_response('No item with specified serial number found', 404)

    return make_response('Item updated successfully', 200)