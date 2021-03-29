import os
from http.client import HTTPSConnection
from base64 import b64encode
from json import loads, dumps
from dotenv import dotenv_values

config = dotenv_values(".env")


class RestClient:
	domain = "api.dataforseo.com"

	def __init__(self, username, password):
		self.username = username
		self.password = password

	def request(self, path, method, data=None):
		connection = HTTPSConnection(self.domain)
		try:
			base64_bytes = b64encode(
				("%s:%s" % (self.username, self.password)).encode("ascii")
			).decode("ascii")
			headers = {'Authorization': 'Basic %s' % base64_bytes, 'Content-Encoding': 'gzip'}
			connection.request(method, path, headers=headers, body=data)
			response = connection.getresponse()
			return loads(response.read().decode())
		finally:
			connection.close()

	def get(self, path):
		return self.request(path, 'GET')

	def post(self, path, data):
		if isinstance(data, str):
			data_str = data
		else:
			data_str = dumps(data)
		return self.request(path, 'POST', data_str)


class Parser:
	client = RestClient(config.get('API_USERNAME'), config.get('API_KEY'))

	def __init__(self, filters, search_engine):
		self.filters = filters
		self.search_engine = search_engine

	def get_task_id(self):
		post_data = dict()
		post_data[len(post_data)] = self.filters
		return self.client.post(f"/v3/serp/{self.search_engine.lower()}/organic/task_post", post_data)['tasks'][0]['id']
