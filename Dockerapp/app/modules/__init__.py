from psycopg2.extras import RealDictCursor
from app.modules.errors import DatabaseError
from flask import g

# Here we define a custom psycopg2 cursor with RealDictCursor as a base. As the name suggests, we are just hooking this into our
# logging and error handling system directly to save ourselves the effort of writing logging queries / try except blocks for each
# database query
class LoggingRealDictCursor(RealDictCursor):

    logger = None

    # Setting logger on startup
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.logger = g.appLogger

    # Changing execute to send queries to our logger and raise DatabaseErrors
    def execute(self, sql, args=None):

        self.logger.info(self.mogrify(sql, args))

        try:
            return super().execute(sql, args)
        except Exception as e:
            self.logger.error(e)
            raise DatabaseError(e)


    # Same as execute, while we aren't using executemany in our implementation it's good to support it for future development
    def executemany(self, sql, args=None):

        self.logger.info(self.mogrify(sql, args))

        try:
            return super().executemany(sql, args)
        except Exception as e:
            self.logger.error(e)
            raise DatabaseError(e)

    # Making it so fetched data (from either fetchone or fetchall) printout to logs
    def fetchall(self):

        try:
            fetchedList = super().fetchall()
            self.logger.info('Fetched Data:\n' + str(fetchedList))
            return fetchedList
        except Exception as e:
            self.logger.error(e)
            raise DatabaseError(e)

    def fetchone(self):

        try:
            fetchedResult = super().fetchone()
            self.logger.info('Fetched Data:\n' + str(fetchedResult))
            return fetchedResult
        except Exception as e:
            self.logger.error(e)
            raise DatabaseError(e)