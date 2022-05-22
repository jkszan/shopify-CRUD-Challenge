from flask import Blueprint, g, make_response, jsonify, request
from app.routes import requires


# This file is used to implement address management, in a proper implementation we would have a full CRUD system for this

address = Blueprint('address', __name__, url_prefix='/address')

@address.route('/',
    methods=['GET'])
def getAddress():

    getQuery = 'SELECT * FROM address'

    g.dbcursor.execute(getQuery)
    addresses = g.dbcursor.fetchall()

    return make_response(jsonify(addresses), 200)


@address.route('/',
    methods=['POST'])
@requires('country', 'state', 'city', 'street', 'house_number', 'postal_code')
def addAddress():

    args = request.args
    country = args.get("country", type=str)
    state = args.get("state", type=str)
    city = args.get("city", type=str)
    street = args.get("street", type=str)
    house_number = args.get("house_number", type=int)
    apt = args.get("apt_specifier", type=str)
    postal_code = args.get("postal_code", type=str)

    insertQuery = '''
        INSERT INTO address(address_country, address_state, address_city, street_name, house_number, apt_specifier, postal_code)
        VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING address_id
    '''

    queryValues = [country, state, city, street, house_number, apt, postal_code]

    g.dbcursor.execute(insertQuery, queryValues)
    address_id = g.dbcursor.fetchone().get('address_id')
    g.dbcon.commit()

    return make_response("Address added successfully under id " + str(address_id), 201)