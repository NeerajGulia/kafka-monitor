from db import DB
from Debugger import Debugger
from topic import Topic
import json

class PandaDB(DB):

    def __init__(self, database, user, password):
        super().__init__(database, user, password)
        # dict 
        self.topics = self.get_all_topics()
        Debugger.printD("PandaDB : init : current topics in db : "+str(self.topics))
    
    def get_all_topics(self):
        self.exe_query("SELECT T_NAME, OFSET, rcd_date FROM TOPIC WHERE ISACTIVE=1;")
        all_topics = self.cur.fetchall()
        topics_dict = {}
        # topics_list = []
        # for topic in all_topics:
        #     topics_set.add(topic[0])
        # return topics_set
        for topic in all_topics:
            t = Topic(topic[0],topic[1],topic[2])
            topics_dict[topic[0]] = t
        print("**** topics dict **** : ",topics_dict)
        return topics_dict
        # topics_set = set()
        # for topic in all_topics:
        #     topics_set.add(topic[0])
        # return topics_set

    def ingest_topics(self, topics, offset_n_time_dict):
        for t in topics:
            try:
                topic_obj = self.topics[t]
                # if topic_obj is not None:
                topic_obj.calc_ar(offset_n_time_dict[t][0], offset_n_time_dict[t][1])
                # self.exe_query("INSERT INTO TOPIC (T_NAME) VALUES "+"(\'"+t+"\');")
                # self.exe_query("INSERT INTO TOPIC (T_NAME,OFSET) VALUES "+"(\'"+t+"\',\'"+str(offset_n_time_dict[t][0])+"\') ON CONFLICT (T_NAME) DO UPDATE SET OFSET = \'"+str(offset_n_time_dict[t][0])+"\';")
                # self.exe_query("INSERT INTO TOPIC_METRIC (T_NAME,AR) VALUES "+"(\'"+t+"\',\'"+str(topic_obj.ar)+"\') ON CONFLICT (T_NAME) DO UPDATE SET OFSET = \'"+str(offset_n_time_dict[t][0])+"\', AR = \'"+str(topic_obj.ar)+"\';")
                self.exe_query("INSERT INTO TOPIC_METRIC (T_NAME, arrival_rate) VALUES "+"(\'"+t+"\',\'"+str(topic_obj.ar)+"\');")
            except:
                pass
            self.exe_query("INSERT INTO TOPIC (T_NAME,OFSET) VALUES "+"(\'"+t+"\',\'"+str(offset_n_time_dict[t][0])+"\') ON CONFLICT (T_NAME) DO UPDATE SET OFSET = \'"+str(offset_n_time_dict[t][0])+"\';")
        self.commit()

    def fetch_arrival_rate_for_last_5_min(self, topic_name):
        # topic_name.decode()
        self.exe_query("SELECT arrival_rate FROM TOPIC_METRIC WHERE T_NAME=\'"+topic_name+"\' ORDER BY RCD_DATE DESC LIMIT 90" )
        ar_fetch = self.cur.fetchall()
        ar_list = []
        for ar in ar_fetch:
            ar_list.append((float)(ar[0]))
        ar_list.reverse()
        # print(ar_list)
        return {'ArrivalRate' : ar_list}




    # def update_ar(self):



    # def update_offset

