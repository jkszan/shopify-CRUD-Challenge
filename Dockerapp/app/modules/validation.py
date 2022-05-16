from app.modules.errors import ParameterError

# Simple function to check for falsy values in Python (i.e. "", [], {}) that indicate an uninstantiated input to required
# variables.
def checkRequiredInput(parameterDict):

    # This converts the input dict to a tuple list and iterates through it
    for parameterName, parameter in parameterDict.items():

        # These values cast to False but are valid inputs
        if parameter == False or parameter == 0 or parameter == 0.0:
            continue

        if not parameter:
            raise ParameterError(parameterName)