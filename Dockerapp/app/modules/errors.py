#This file exists as a place to define custom errors

# DatabaseError is a wrapper for any other error that props up as a part of a database transaction. We need to store
# the source error to properly access Postgres error information
class DatabaseError(Exception):
    status_code = 400
    description = "DatabaseError: Exception encountered during database interaction"
    sourceError = None
    def __init__(self, originalError = None):

        if originalError:
            self.sourceError = originalError

class ParameterError(Exception):
    status_code = 400
    description = "ParameterError: Malformed input, required variable not provided"

    def __init__(self, variableName=""):

        if variableName:
            self.description = "ParameterError: Required variable " + variableName + " not provided"

class InputError(Exception):
    status_code = 400
    description = "InputError: Malformed input"

    def __init__(self, errorDescription=""):

        if errorDescription:
            self.description = "InputError: " + errorDescription