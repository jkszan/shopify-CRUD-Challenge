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

    g.appLogger.error(errorReturn)

    if hasattr(exception, 'description'):
        return make_response(exception.description, 400)

    return make_response(str(exception), 400)

# For database errors, we want to give the cause of the error without internal
# information to the user
@errorhandler.app_errorhandler(DatabaseError)
def databaseErrorHandler(exception):

    # If the DatabaseException does not have postgres error information, we default to standard error
    try:
        errorReturn = getPsycopg2Exception(exception.sourceError)
    except Exception as e:
        errorReturn = {
                'Exception' : exception.description,
                'Traceback' : traceback.format_exc()
                }

    g.appLogger.error(errorReturn)
    return make_response(jsonify(errorReturn['Exception']), exception.status_code)

@errorhandler.app_errorhandler(404)
def notFound(exception):
    errorReturn = {
        'Message' : '404: URI not found',
        'Request'   : str(request),
        'Exception' : str(exception)
    }
    g.appLogger.error(errorReturn)

    return make_response(jsonify(errorReturn['Exception']), 404)

@errorhandler.app_errorhandler(405)
def unauthorized(exception):
    errorReturn = {
        'Message' : '404: Unauthorized',
        'Request'   : str(request),
        'Exception' : str(exception)
    }
    g.appLogger.error(errorReturn)

    return make_response(jsonify(errorReturn['Exception']), 404)

# Simple function to get some extra information for database errors
def getPsycopg2Exception(databaseError):
    from psycopg2 import OperationalError, errorcodes, errors

    errorSpec = {
                "Traceback": traceback.format_exc(),
                "Exception": databaseError.pgerror,
                "Code": databaseError.pgcode
                }

    return errorSpec

# Some simple /error routes to test exception handlers
@errorhandler.route('/',
    methods=['GET'])
def generalError():
    raise Exception('Test General Exception')

@errorhandler.route('/databaseError',
    methods=['GET'])
def databaseError():
    raise DatabaseError('Test Database Error')

@errorhandler.route('/404',
    methods=['GET'])
def notFoundtester():
    raise NotFound('Test 404 Error')

@errorhandler.route('/405',
    methods=['GET'])
def unauthorizedtester():
    raise MethodNotAllowed('Test 405 Error')