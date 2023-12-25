from repository.utils.IRepository import IRepository

from mysql.connector import connect, Error


class ConnectionExpired(Error):
    pass


class MySQLRepository(IRepository):

    def __init__(self, user, password, database, host='127.0.0.1', port='3306'):
        self.user = user
        self.password = password
        self.database = database
        self.host = host
        self.port = port

    def executeSqlQuery(self, conn, queryStr: str, argsValues=None):

        cursor = conn.cursor()

        if argsValues is None:
            cursor.execute(queryStr)
        else:
            cursor.execute(queryStr, argsValues)

        responseSql = cursor.fetchall()
        queryStrToUpper = queryStr.upper()
        if 'SELECT' in queryStrToUpper:
            response = [list(row) for row in responseSql]
        else:
            response = None

        return response

    def checkConnection(self, connection):
        if connection is not None:
            if connection.is_connected():
                return True
            else:
                return False
        else:
            return False

    def getConnection(self):
        return connect(user=self.user, password=self.password, database=self.database, host=self.host, port=self.port)

