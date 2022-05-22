from flask import Flask, g, send_from_directory, render_template
from flask_cors import CORS
from app.routes import inventory, item, errorhandler, product, address
from app.modules import LoggingRealDictCursor
import psycopg2
import os


# Setting configuration info from definition in the config directory
def setConfigInfo():

    # This method is a proof of concept on how you could use the config system in the future for different deployment types

    if os.environ['APIMODE'] == 'development':
        flaskapp.config.from_object('app.config.DebugConfig')
    else:
        flaskapp.config.from_object('app.config.Config')

    flaskapp.logger.setLevel(flaskapp.config['LOG_LEVEL'])
    flaskapp.url_map.strict_slashes == False

# Helper function to get a database connection, setting default cursor to a custom-made logging cursor
def getConn():

    db_config = {
        "host" : flaskapp.config['SQLHOST'],
        "dbname" : flaskapp.config['SQLDB'],
        "user" : flaskapp.config['SQLUSER'],
        "password" : flaskapp.config['SQLPASSWORD']
    }

    dbcon = psycopg2.connect(cursor_factory=LoggingRealDictCursor, **db_config)

    return dbcon

# Instantiating our app
flaskapp = Flask(__name__)
setConfigInfo()

# We are using CORS due to some authentification issues with Swagger-UI
CORS(flaskapp)


# This method sets up request-level variables on each request
@flaskapp.before_request
def beforeRequest():

    g.appLogger = flaskapp.logger

    # Instantiating our database connection and cursor
    g.dbcon = getConn()
    g.dbcursor = g.dbcon.cursor()


# This method cleans any remaining database connections after request completion
@flaskapp.teardown_appcontext
def close_db(error):

    if hasattr(g, 'dbcursor'):
        g.dbcursor.close()

    if hasattr(g, 'dbcon'):
        g.dbcon.close()

# Route at the root of the app directing users to the swagger instance
@flaskapp.route('/')
def index():
    return render_template('swagger.html')

# Simple route to define which file should be used for the page icon (Its a nice touch, I think)
@flaskapp.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(flaskapp.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')


# Registering our route Blueprints. It's annoying to do it this way and it's possible to iterate through all files in the routes folder and register [filename.filename] for each, but this
# is much easier for future maintainers to understand. Preferably you would have both but generally I believe that readability and maintainability are much more important than visually appealing
# solutions
selectedBlueprints = [inventory.inventory, product.product, item.item, errorhandler.errorhandler, address.address]

for blueprint in selectedBlueprints:
    flaskapp.register_blueprint(blueprint)
    flaskapp.logger.info('Registered Blueprint ' + blueprint.name)