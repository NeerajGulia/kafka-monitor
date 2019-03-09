import json
from flask import request, abort, jsonify
from flask_restful import Resource, reqparse
import os
from flask import render_template
import time
import logging
from api import api, monitor, kafka_brokers

log = logging.getLogger(__name__) 

class Topic(Resource):
    def get(self, topic):
        return monitor.Monitor(kafka_brokers).desc_topic(topic.encode())

class TopicConsumersLag(Resource):
    def __init__(self, *args, **kwargs):
            super(TopicConsumersLag, self).__init__()
            
    def get(self, topic):
        return  monitor.Monitor(kafka_brokers).get_topic_consumers_lag(topic.encode())

class TopicConsumers(Resource):
    def __init__(self, *args, **kwargs):
            super(TopicConsumers, self).__init__()
            
    def get(self):
        return  monitor.Monitor(kafka_brokers).get_topics_consumers()

class TopicList(Resource):
    def __init__(self, *args, **kwargs):
            self.parser = reqparse.RequestParser()
            super(TopicList, self).__init__()
            
    def get(self):
        return  [y.decode() for y in monitor.Monitor(kafka_brokers).get_topics()] 

class Help(Resource):
    def get(self):
        return [{'/api/topics': 'get all topics'},
                {'/api/topicconsumers': 'get all topics with respective consumers'},
                {'/api/topicconsumerslag/<string:topic>': 'get consumers lag for given topic'}, 
                {'/api/topic/<string:topic>': 'get topic description for given topic'}
				]

api.add_resource(Help, '/api/help')     
api.add_resource(TopicList, '/api/topics')
api.add_resource(TopicConsumers, '/api/topicconsumers')
api.add_resource(TopicConsumersLag, '/api/topicconsumerslag/<string:topic>')
api.add_resource(Topic, '/api/topic/<string:topic>')