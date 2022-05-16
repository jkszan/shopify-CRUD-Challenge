from psycopg2.extras import RealDictCursor
from flask import g

# Making a simple custom psycopg2 cursor to log queries while using the RealDictCursor implementation
class LoggingRealDictCursor(RealDictCursor):

    logger = None

    # Setting logger
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.logger = g.appLogger

    # Implementing behavior to log every DB query
    def execute(self, sql, args=None):

        self.logger.info(self.mogrify(sql, args))

        try:
            return super().execute(sql, args)
        except Exception as e:
            self.logger.error(e)
            raise

    # fetchall and fetchone add logging to *fetched* query results, DELETE, INSERT or UPDATE statements will only clog up the logs
    def fetchall(self):

        try:
            fetchedList = super().fetchall()
            self.logger.info('Fetched Data:\n' + str(fetchedList))
            return fetchedList
        except Exception as e:
            self.logger.error(e)
            raise

    def fetchone(self):

        try:
            fetchedResult = super().fetchone()
            self.logger.info('Fetched Data:\n' + str(fetchedResult))
            return fetchedResult
        except Exception as e:
            self.logger.error(e)
            raise