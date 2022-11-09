from utils.functions import interval
from threading import Thread
from copy import deepcopy
from uuid import uuid4
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
		for idx, file_infor in enumerate(deepcopy(data_file)):
			if file_infor["expiresAt"] < time.time():
				try:
					os.remove(file_infor["path"])
				except Exception as e:
					print(e)
				del data_file[idx]
		self.writeJson(data=data_file)


	def reValidate(self, path, expiresAt=30):
		data_file = self.readJson(self.data_file)
		for file_infor in data_file:
			if file_infor["path"] == path:
				file_infor["expiresAt"] = time.time() + (expiresAt * 60)
		self.writeJson(data=data_file)


	def addPath(self, path, expiresAt=30):
		data_file = self.readJson(self.data_file)
		fc = lambda file_infor: file_infor.path != path
		data_file = list(filter(fc, data_file))
		data_file.append({
			"path": path,
			"id": str(uuid4()),
			"expiresAt": time.time() + (expiresAt * 60) # + 30 minutes
		})
		self.writeJson(data=data_file)


	def getFilePathById(uid):
		data_file = self.readJson(self.data_file)
		for file_infor in data_file:
			if file_infor["id"] == uid:
				return file_infor["path"]