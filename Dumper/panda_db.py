from db import DB
from Debugger import Debugger

class PandaDB(DB):

    def __init__(self, database, user, password):
        super().__init__(database, user, password)
        self.topics = self.get_all_topics()
        Debugger.printD("PandaDB : init : current topics in db : "+str(self.topics))
    
    def get_all_topics(self):
        self.exe_query("SELECT T_NAME,OFSET,TIMESTAMP FROM TOPIC WHERE ISACTIVE=1;")
        all_topics = self.cur.fetchall()
        topics_dict = {}
        # topics_list = []
        # for topic in all_topics:
        #     topics_set.add(topic[0])
        # return topics_set
        for topic in all_topics:
            t = Topic(topic[0],topic[1],topic[1])
            topics_dict[topic[0]] = t
        print("**** topics dict **** : ",topics_dict)
        return topics_dict
        # topics_set = set()
        # for topic in all_topics:
        #     topics_set.add(topic[0])
        # return topics_set

    def ingest_topics(self, topics_diff_set,offset_dict):
        for t in topics_diff_set:
            # self.exe_query("INSERT INTO TOPIC (T_NAME) VALUES "+"(\'"+t+"\');")
            self.exe_query("INSERT INTO TOPIC (T_NAME,OFSET) VALUES "+"(\'"+t+"\',\'"+str(offset_dict[t])+"\') ON CONFLICT (T_NAME) DO UPDATE SET OFSET = \'"+str(offset_dict[t])+"\';")
        self.commit()

    def update_ar(self):



    # def update_offset

