from threading import Thread
from utils.functions import interval
import json
import time


class Collector:
	def __init__(self):
		super(Collector, self).__init__()
		self.data_file = "collector_data.json"


	def start(self, gap=30):
		interval(self.checkFiles, gap * 60)


	def checkFiles(self):
		data_file = json.load(self.data_file)
		timestamp = time.time()