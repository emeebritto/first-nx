from threading import Thread
from utils.functions import interval
from copy import deepcopy
import json
import time
import os

class Collector:
	def __init__(self):
		super(Collector, self).__init__()
		self.data_file = "collector_data.json"
		if not os.path.exists(self.data_file): self.writeJson()
		else: self.checkFiles()


	def readJson(self, path):
		with open(path, 'r') as json_data:
			return json.load(json_data)


	def writeJson(self, data={}):
		data_file = open(self.data_file, "w")
		json.dump(data, data_file, indent=2)
		data_file.close()


	def start(self, gap=5):
		interval(self.checkFiles, gap * 60)


	def checkFiles(self):
		data_file = self.readJson(self.data_file)
		new_data_file = []
		for path, expiresAt in deepcopy(data_file).items():
			if expiresAt < time.time():
				try:
					os.remove(path)
				except Exception as e:
					print(e)
			del data_file[path]
		self.writeJson(data=data_file)


	def reValidate(self, path, expiresAt=30):
		self.addPath(path, expiresAt=expiresAt)


	def addPath(self, path, expiresAt=30):
		data_file = self.readJson(self.data_file)
		data_file[path] = time.time() + (expiresAt * 60) # + 30 minutes
		self.writeJson(data=data_file)
