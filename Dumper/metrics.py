from pykafka import KafkaClient
from Debugger import Debugger
import time


class Metric:
	
	def __init__(self, host , port):
		self.create_client(host, port)
		self.get_current_topics()
	
	def create_client(self, host, port):
		self.client = KafkaClient(hosts=host + ':' + port)
		Debugger.printD("Metric : create_client : Client "+host + ':' + port + "created Successfully") 

	def get_offset_by_topic(self, topic):
		return topic.latest_available_offsets()
		
	def get_current_topics(self):
		self.current_topics = self.client.topics
		Debugger.printD("Metric : get_current_topics : "+ str(type(self.current_topics)))

	



