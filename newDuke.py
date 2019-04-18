import sqlite3
from threading import Thread




class SQEXEC:
    major_connection = None
    major_cursor = None

    def __init__(self, connection, cursor):
        global major_connection, major_cursor
        major_connection = connection
        major_cursor = cursor
        #connection = sqlite3.connect('example.db')
        #cursor = connection.cursor()
        pass

        
    def run(self):
        global major_connection, major_cursor
        sql_1 = """
        CREATE TABLE IF NOT EXISTS Chatty(log TEXT);
        """

        sql_2 = """
        INSERT INTO Chatty VALUES('wO3WO');
        """
        major_cursor.execute(sql_1)
        major_cursor.execute(sql_2)
        major_connection.commit()
        major_connection.close()

        print("Executed")
        

_connection = sqlite3.connect('Example.db')
_cursor = _connection.cursor()



if __name__ == "__main__":
    mySQE = SQEXEC(_connection, _cursor)
    mySQE.run()
#Thread t1 = Thread(target=)

