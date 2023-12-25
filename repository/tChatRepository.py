from repository.utils.IRepository import IRepository
import datetime
from exceptions.UserNotCreatedYet import UserNotCreatedYet


class TChatRepository:

    def __init__(self, repository: IRepository):
        self.repository = repository
        self.connection = None

    def checkConnection(self):

        if self.connection is None:
            return False

        if self.repository.checkConnection(self.connection):
            return True
        else:
            return False
        # return True

    def setConnection(self):
        self.connection = self.repository.getConnection()

    def addMessage(self, senderId: int, receiverLogin, messageText, imageBinaryData=None, imageExtension=None):

        if not self.checkConnection():
            self.setConnection()

        receiverIdQuery = """
        SELECT id, login FROM users users
        WHERE users.id IS NOT NULL 
        AND users.login=%s
        """

        keys = ['id', 'login']


        receiverQueryResponse = self.repository.executeSqlQuery(conn=self.connection, queryStr=receiverIdQuery,
                                                                argsValues=(receiverLogin,))

        if len(receiverQueryResponse) == 0:
            raise UserNotCreatedYet

        receiverData = []

        for row in receiverQueryResponse:
            receiverData.append({keys[idx]: val for idx, val in enumerate(row)})

        receiverId = receiverData[0]['id']

        if imageBinaryData is None:
            queryStr = """
            INSERT INTO messages (sender, receiver, text, date) VALUES (%s, %s, %s, %s)
            """
            self.repository.executeSqlQuery(conn=self.connection, queryStr=queryStr,
                                            argsValues=(senderId, receiverId, messageText, datetime.datetime.utcnow(),))
        else:
            queryStr = """
            INSERT INTO messages (sender, receiver, text, image, image_extension, date) VALUES (%s, %s, %s, %s, %s, %s)
            """
            self.repository.executeSqlQuery(conn=self.connection, queryStr=queryStr,
                                            argsValues=(
                                                senderId, receiverId, messageText, imageBinaryData,
                                                imageExtension, datetime.datetime.utcnow(),
                                            )
                                            )

        self.connection.commit()

    def addUser(self, userLogin: str, hashedPassword: str):

        if not self.checkConnection():
            self.setConnection()

        queryStr = """
        INSERT INTO users (login, password) VALUES (%s, %s)
        """

        self.repository.executeSqlQuery(conn=self.connection, queryStr=queryStr,
                                        argsValues=(userLogin, hashedPassword,))

        self.connection.commit()
        return True

    def getUserInfoByLogin(self, userLogin):
        if not self.checkConnection():
            self.setConnection()

        queryStr = """
        SELECT id, login, password FROM users users
        WHERE users.id IS NOT NULL 
        AND users.login=%s
        """

        keys = ['id', 'login', 'password']

        responseList = self.repository.executeSqlQuery(conn=self.connection, queryStr=queryStr,
                                                       argsValues=(userLogin,))

        response = []

        for row in responseList:
            response.append({keys[idx]: val for idx, val in enumerate(row)})

        self.connection.commit()
        return response[0]

    def getMessageById(self, messageId):

        if not self.checkConnection():
            self.setConnection()

        queryStr = """
        SELECT messages.id, text, image, image_extension, receiver.login as receiver_login, sender.login as sender_login, messages.date as date
        FROM messages messages
        INNER JOIN users AS receiver ON messages.receiver=receiver.id
        INNER JOIN users AS sender ON messages.sender=sender.id
        WHERE messages.id IS NOT NULL
        AND messages.id=%s
        """

        keys = ['id', 'text', 'image', 'image_extension', 'receiver_login', 'sender_login', 'date']

        responseList = self.repository.executeSqlQuery(conn=self.connection, queryStr=queryStr,
                                                       argsValues=(messageId,))

        response = []

        for row in responseList:
            response.append({keys[idx]: val for idx, val in enumerate(row)})

        self.connection.commit()
        return response[0]

    def getAllMessagesByUserLogin(self, userLogin: str):

        if not self.checkConnection():
            self.setConnection()

        queryStr = """
        SELECT messages.id as id, text, receiver.login as receiver_login, sender.login as sender_login, messages.date as date
        FROM messages messages
        INNER JOIN users AS receiver ON messages.receiver=receiver.id
        INNER JOIN users AS sender ON messages.sender=sender.id
        WHERE receiver.login IS NOT NULL
        AND receiver.login=%s
        ORDER BY messages.date
        """

        keys = ['id', 'text', 'receiver_login', 'sender_login', 'date']

        responseList = self.repository.executeSqlQuery(conn=self.connection, queryStr=queryStr,
                                                       argsValues=(userLogin,))

        response = []

        for row in responseList:
            response.append({keys[idx]: val for idx, val in enumerate(row)})

        self.connection.commit()
        return response
