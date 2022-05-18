from flask import Blueprint, g, make_response, jsonify, request
from app.modules.errors import DatabaseError
from app.modules.validation import checkRequiredInput


# This file is used to implement address management, in a proper implementation we would have a full CRUD system for this

address = Blueprint('address', __name__, url_prefix='/address')

@address.route('/',
    strict_slashes=False,
    methods=['GET'])
def getAddress():

    getQuery = 'SELECT * FROM address'

    try:
        g.dbcursor.execute(getQuery)
        addresses = g.dbcursor.fetchall()
    except Exception as e:
        raise DatabaseError(e)

    return make_response(jsonify(addresses), 200)


@address.route('/',
    strict_slashes=False,
    methods=['POST'])
def addAddress():

    args = request.args

    country = args.get("country", default="", type=str)
    state = args.get("state", default="", type=str)
    city = args.get("city", default="", type=str)
    street = args.get("street", default="", type=str)
    house_number = args.get("house_number", default="", type=int)
    apt = args.get("apt_specifier", default="", type=str)
    postal_code = args.get("postal_code", default="", type=str)

    checkRequiredInput({"Country": country, "State": state, "City": city, "Street": street, "House Number": house_number, "Postal Code": postal_code})

    insertQuery = '''
        INSERT INTO address(address_country, address_state, address_city, street_name, house_number, apt_specifier, postal_code)
        VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING address_id
    '''

    queryValues = [country, state, city, street, house_number, apt, postal_code]

    try:
        g.dbcursor.execute(insertQuery, queryValues)
        address_id = g.dbcursor.fetchone().get('address_id')
        g.dbcon.commit()
    except Exception as e:
        raise DatabaseError(e)

    return make_response("Address added successfully under id " + str(address_id), 201)
