from flask import g
from app.modules.errors import InputError

def getProductID(productName):
    query = 'SELECT product_id as id FROM product WHERE product_name = %s'
    return __getID(productName, query, 'product_id')

def getInventoryID(inventoryName):
    query = 'SELECT inventory_id as id FROM inventory WHERE inventory_name = %s'
    return __getID(inventoryName, query, 'inventory_id')

# General getID helper function, can be expanded to implement ID fetching other tables where necesary
def __getID(name, query, column_name):

    # If the name is already all digits, assume that ID has been passed as input
    if name.isdigit():
        return name

    g.dbcursor.execute(query, name)
    resultIDs = g.dbcursor.fetchall()


    if len(resultIDs) > 1:
        raise InputError('Multiple entries returned for ' + column_name)

    if len(resultIDs) < 1:
        raise InputError('No results returned for ' + column_name)

    # Because of the above if statements, we know there is one entry to the result list
    return resultIDs[0].get('id')