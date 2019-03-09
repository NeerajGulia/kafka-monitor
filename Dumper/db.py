import psycopg2
from Debugger import Debugger

class DB:
    def __init__(self, database, user, password, host="127.0.0.1", port = "5432"):
        self.conn = psycopg2.connect(database = database, user = user, password = password, host = host, port = port)
        self.cur = self.conn.cursor()
        # conn = psycopg2.connect("dbname = "+database+", user = "+user+", password = "+password+", host = "+host+", port = "+port)
        Debugger.printD("DB : init : database "+database+" connected successfully...")

    def exe_query(self,query):
        self.cur.execute(query)

    def close(self):
        self.conn.close()
    
    def commit(self):
        self.conn.commit()
    

    
