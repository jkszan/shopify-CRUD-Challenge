import os

class Config(object):
    SQLHOST = os.environ["HOST"]
    SQLUSER = os.environ["DBUSER"]
    SQLPASSWORD = os.environ["DBPASS"]
    SQLDB = os.environ["DATABASE"]
    APIPORT = os.environ["APIPORT"]
    LOG_LEVEL = 'INFO'

class DebugConfig(Config):
    LOG_LEVEL = 'DEBUG'