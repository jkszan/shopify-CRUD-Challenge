from flask import Blueprint, g, jsonify, make_response, request
from werkzeug.exceptions import MethodNotAllowed, NotFound
from app.modules.errors import DatabaseError
import traceback

errorhandler = Blueprint('error', __name__, url_prefix='/error')

# This file works as a place to define error handling behavior across the Flask app. You can define error handlers on custom errors and differentiate
# output based on the configuration of the Flask app (i.e. Giving more log printout based on set log level or providing verbose output to users in debug mode)

@errorhandler.app_errorhandler(Exception)
def exceptionHandler(exception):
    errorReturn = {
                'Request'   : str(request),
                'Exception' : str(exception),
                'Traceback' : traceback.format_exc()
                }

    # We return intensive error info to logs and a simple error message to the user to make this more user-friendly and avoid showing potentially
    # sensitive information about our internal system
    g.appLogger.error(errorReturn)

    # Its possible to make an exhaustive system that captures every error raised in execution and gives each a status code to get and
    # return here. For this demo we will just statically define it to be 400

    if hasattr(exception, 'description'):
        return make_response(exception.description, 400)

    return make_response(str(exception), 400)

@errorhandler.app_errorhandler(DatabaseError)
def databaseErrorHandler(exception):


    try:
        errorSpec = getPsycopg2Exception(exception.sourceError)
    except Exception as e:
        errorSpec = {
                'Error' : exception.description,
                'Traceback' : traceback.format_exc()
                }

    g.appLogger.error(errorSpec)
    return make_response(jsonify(errorSpec['Error']), exception.status_code)

@errorhandler.app_errorhandler(404)
def notFound(exception):
    errorReturn = {
        'Message' : '404: URI not found',
        'Request'   : str(request),
        'Exception' : str(exception)
    }
    g.appLogger.error(errorReturn)

    return exception

@errorhandler.app_errorhandler(405)
def unauthorized(exception):
    errorReturn = {
        'Message' : '404: Unauthorized',
        'Request'   : str(request),
        'Exception' : str(exception)
    }
    g.appLogger.error(errorReturn)

    return exception

def getPsycopg2Exception(databaseError):
    from psycopg2 import OperationalError, errorcodes, errors

    errorSpec = {
                "Traceback": traceback.format_exc(),
                "Error": databaseError.pgerror,
                "Code": databaseError.pgcode
                }

    return errorSpec

@errorhandler.route('/',
    strict_slashes=False,
    methods=['GET'])
def generalError():
    raise Exception('Testing Database Error')

@errorhandler.route('/databaseError',
    strict_slashes=False,
    methods=['GET'])
def databaseError():
    raise DatabaseError('Testing Database Error')

@errorhandler.route('/404',
    strict_slashes=False,
    methods=['GET'])
def notFoundtester():
    raise NotFound('Testing 404 Error')

@errorhandler.route('/405',
    strict_slashes=False,
    methods=['GET'])
def unauthorizedtester():
    raise MethodNotAllowed('Testing 405 Error')

