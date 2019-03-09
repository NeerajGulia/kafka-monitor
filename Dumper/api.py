import flask
import requests

API_HOST = "http://13.234.16.29:10001/api"
from Debugger import Debugger

class API:

    def __init__(self):
        # api = flask.Flask(__name__)
        Debugger.printD("API : api created successfully...")

    # returns list of topics - set
    def get_topics(self):
        topics = self.get('/topics')
        Debugger.printD("API : get_topics : topics : "+ str(type(topics.json())) +" "+str(topics.json()))
        return (topics.json())

    def get_all_offsets(self, topics):
        offset_dict = {}
        for t in topics:
            offset = self.get_topic_info(t)['Latest_Offset']
            offset_dict[t] = offset
        return offset_dict

    # returns dict of topic info
    def get_topic_info(self, topic_name):
        topic_info = self.get("/topic/"+topic_name)
        Debugger.printD("API : get_topic_info : info : "+ str(type(topic_info.json())) +" "+str(topic_info.json()))
        return topic_info.json()

    def get_all_consumers(self):
        cons = self.get("/topicconsumers")
        Debugger.printD("API : get_all_consumers : lag : "+ str(type(cons.json())) +" "+str(cons.json()))
        return cons.json()

    # returns list of consumers and lag
    def get_consumers_n_lag_by_topic(self, topic_name):
        lag = self.get("/topicconsumerslag/"+topic_name)
        Debugger.printD("API : get_consumers_n_lag_by_topic : lag : "+ str(type(lag.json())) +" "+str(lag.json()))
        return lag.json()

    def get(self, path):
        resp = requests.get(API_HOST+path)
        if resp.status_code != 200:
            raise Exception('GET : '+path+' Response Code : {}'.format(resp.status_code))
        # Debugger.printD("API : get : "+ str(resp.json()))
        return resp

    # TODO : add api for offset
    # def get_offset()


# for todo_item in resp.json():
#     print('{} {}'.format(todo_item['id'], todo_item['summary']))