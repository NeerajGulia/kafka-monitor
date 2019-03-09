from panda_db import PandaDB
from api import API
from Debugger import Debugger

DATABASE = "panda"
USER = "postgres"
PASSWORD = "postgres"

class Dumper:
    def __init__(self):
        self.panda_db = PandaDB(DATABASE, USER, PASSWORD)
        Debugger.printD("DUMPER : init : DUMPER created successfully...")
        self.api = API()
        self.topics = self.api.get_topics()
        Debugger.printD("DUMPER : init : self.topics "+ str(self.topics))

    def ingest_latest_topics(self):
        # topic_diff = self.topics.difference(self.panda_db.topics)
        offset_dict = self.api.get_all_offsets(self.topics)
        # offset_dict = {}
        # for t in self.panda_db.topics:
        #     offset = self.api.get_topic_info(t)['Latest_Offset']
        #     offset_dict[t] = offset
        print('offset_dict : ',offset_dict)
        # print("topic_diff : " ,topic_diff)
        self.panda_db.ingest_topics(self.topics, offset_dict)


dumper = Dumper()
dumper.ingest_latest_topics()


# api.get_topics()
# api.get_topic_info('test')
	