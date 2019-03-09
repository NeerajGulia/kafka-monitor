from pykafka import KafkaClient
import pykafka
from pykafka.common import OffsetType
from pykafka.protocol import PartitionOffsetCommitRequest, CreateTopicRequest
from pykafka.utils.compat import PY3, iteritems
import datetime as dt

class Monitor:
	def __init__(self, kafka_brokers=['localhost:9092']):
		self.client = KafkaClient( ",".join(kafka_brokers))

	def get_topics(self):
		return self.client.topics.keys()
	
	def desc_topic(self, topic):
		if topic not in self.client.topics:
			return {'status':'Error, topic {} does not exist'.format(topic)}
		top = self.client.topics[topic]
		desc = []
		partition_count = 0
		replica_count = 0
		isr_count = 0
		latest_offset = 0
		for p in top.partitions.values():
			partition_count += 1
			replica_count += len(p.replicas)
			isr_count += len(p.isr)
			latest_offset = p.latest_available_offset()
		return {
				'Partitions':partition_count,
				'Replicas': replica_count,
				'ISR': isr_count,
				'Latest_Offset': latest_offset
				}
	
	def get_topics_consumers(self):
		pair = {}
		for topic in self.get_topics():
			pair[topic.decode()] = [y.decode() for y in self.get_consumer(topic)]
		return [pair]
	
	def get_topic_consumers_lag(self, topic):
		consumers_list = []
		for consumer in self.get_consumer(topic):
			consumers_list.append(self.get_consumer_lag(topic, consumer))
		output = self.desc_topic(topic)
		output['consumers'] = consumers_list
		return output
	
	def get_consumer(self, topic):
		if topic not in self.client.topics:
			return {'status':'Error, topic {} does not exist'.format(topic)}
		brokers = self.client.brokers
		consumers = []
		for broker_id, broker in iteritems(brokers):
			groups = broker.list_groups().groups.keys()
			groups_metadata = broker.describe_groups(group_ids=groups).groups
			for group_id, describe_group_response in iteritems(groups_metadata):
				members = describe_group_response.members
				for member_id, member in iteritems(members):
					topics = member.member_metadata.topic_names
					if topic in topics:
						consumers.append(describe_group_response.group_id)
		return consumers
	
	def fetch_offsets(self, topic, offset):
		"""Fetch raw offset data from a topic.
		:param topic:  Name of the topic.
		:type topic:  :class:`pykafka.topic.Topic`
		:param offset: Offset to fetch. Can be earliest, latest or a datetime.
		:type offset: :class:`pykafka.common.OffsetType` or
			:class:`datetime.datetime`
		:returns: {partition_id: :class:`pykafka.protocol.OffsetPartitionResponse`}
		"""
		if offset.lower() == 'earliest':
			return topic.earliest_available_offsets()
		elif offset.lower() == 'latest':
			return topic.latest_available_offsets()
		else:
			offset = dt.datetime.strptime(offset, "%Y-%m-%dT%H:%M:%S")
			offset = int(calendar.timegm(offset.utctimetuple()) * 1000)
			return topic.fetch_offset_limits(offset)
			
	def get_consumer_lag(self, topic, consumer_group):
		"""Get raw lag data for a topic/consumer group.
		:param topic:  Name of the topic.
		:type topic:  :class:`pykafka.topic.Topic`
		:param consumer_group: Name of the consumer group to fetch lag for.
		:type consumer_groups: :class:`str`
		:returns: dict of {partition_id: (latest_offset, consumer_offset)}
		"""
		if topic not in self.client.topics:
			return {'status':'Error, topic {} does not exist'.format(topic)}
		top = self.client.topics[topic]
		latest_offsets = self.fetch_offsets(top, 'latest')
		consumer = top.get_simple_consumer(consumer_group=consumer_group,
											 auto_start=False,
											 reset_offset_on_fetch=False)
		current_offsets = consumer.fetch_offsets()
		pid_dict = {}
		for p_id, stat in current_offsets:
			pid_dict[p_id] = (latest_offsets[p_id].offset[0], stat.offset)
		lag_list = []
		consumer_details = {}
		consumer_details['name'] = consumer_group.decode()
		for k,v in iteritems(pid_dict):
			d = {
				'Partition': k,
				'Lag': v[0] - v[1],
				'Latest Offset': v[0],
				'Current Offset': v[1],
				#'Consumer_ID': v[2],
				#'Client_ID': v[3]
			}
			lag_list.append(d)
		consumer_details['partitions'] = lag_list
		return consumer_details