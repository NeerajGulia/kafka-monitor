from panda_db import PandaDB
from api import API
from Debugger import Debugger
import time

DATABASE = "panda"
USER = "postgres"
PASSWORD = "postgres"

REFRESH_RATE = 10

class Dumper:
    def __init__(self):
        self.panda_db = PandaDB(DATABASE, USER, PASSWORD)
        Debugger.printD("DUMPER : init : DUMPER created successfully...")
        self.api = API()
        self.topics = self.api.get_topics()
        Debugger.printD("DUMPER : init : self.topics "+ str(self.topics))

    def fetch_latest_topics(self):
        self.topics = self.api.get_topics()

    def ingest_latest_topics(self):
        # topic_diff = self.topics.difference(self.panda_db.topics)
        offset_n_time_dict = self.api.get_all_offsets(self.topics)
        # offset_dict = {}
        # for t in self.panda_db.topics:
        #     offset = self.api.get_topic_info(t)['Latest_Offset']
        #     offset_dict[t] = offset
        # print('offset_n_time_dict : ',offset_n_time_dict)   
        # print("topic_diff : " ,topic_diff)
        self.panda_db.ingest_topics(self.topics, offset_n_time_dict)


dumper = Dumper()
dumper.ingest_latest_topics()

while(1):
    time.sleep(REFRESH_RATE)
    print("Main : start updating Database....")
    print("Main : fetching Latest Topics....")
    dumper.fetch_latest_topics()
    print("Main : ingesting Latest Topics in DB....")
    dumper.ingest_latest_topics()

	