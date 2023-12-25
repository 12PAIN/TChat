from abc import abstractmethod, ABC

class IRepository(ABC):

    @abstractmethod
    def executeSqlQuery(self, conn, queryStr, argsValues=None):
        raise NotImplementedError

    @abstractmethod
    def getConnection(self):
        raise NotImplementedError

    @abstractmethod
    def checkConnection(self, connection):
        raise NotImplementedError
