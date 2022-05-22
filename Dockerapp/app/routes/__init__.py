from flask import request
from app.modules.errors import ParameterError
from functools import wraps

# This set of functions work to define the @requires wrapper, this handles
# the verification of required parameters being provided to an endpoint
def requires(*requiredParameters):
    def requiresDecorator(endpoint):
        @wraps(endpoint)
        def validateParameters(*args, **kwargs):

            # The empty string is not a valid input for required parameters
            invalidInputs = [None, '']
            for parameterName in requiredParameters:
                if request.args.get(parameterName) in invalidInputs:
                    raise ParameterError(parameterName)

            return endpoint(*args, **kwargs)
        return validateParameters
    return requiresDecorator