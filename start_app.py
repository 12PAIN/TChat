from model.model import MainAppModel
from repository.tChatRepository import TChatRepository

from repository.utils.MySQLRepository import MySQLRepository

if __name__ == "__main__":

    mySqlRep = MySQLRepository(user='dataBaseInstanceUser', password='dbPassword1', database='t_chat', host='127.0.0.1', port='3306')

    rep = TChatRepository(mySqlRep)
    model = MainAppModel(rep)


