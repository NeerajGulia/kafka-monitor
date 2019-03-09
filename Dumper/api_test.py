from db import DB
from api import API

DATABASE = "panda"
USER = "postgres"
PASSWORD = "postgres"

#if __name__=='main':

# panda_db = DB(DATABASE, USER, PASSWORD)
api = API()

api.get_topics()
api.get_topic_info('test')
api.get_all_consumers()
api.get_consumers_n_lag_by_topic('test')
