from copy import deepcopy
from uuid import uuid4
import time
import json
import os


class Room_Managet:
	def __init__(self):
		super(Room_Managet, self).__init__()
		self.data_file = "room_manager.json"
		if not os.path.exists(self.data_file): self.writeJson()


	def readJson(self, path):
		with open(path, 'r') as json_data:
			return json.load(json_data)


	def writeJson(self, data=[]):
		data_file = open(self.data_file, "w")
		json.dump(data, data_file, indent=2)
		data_file.close()


	def checkKeys(self):
		data_file = self.readJson(self.data_file)
		for idx, key in enumerate(deepcopy(data_file)):
			if key["expiresAt"] < time.time():
				del data_file[idx]
		self.writeJson(data=data_file)


	def create_key(self, label):
		self.checkKeys()
		data_file = self.readJson(self.data_file)
		obj_key = {
			"label": label,
			"key": str(uuid4()).replace("-", ""),
			"expiresAt": time.time() + (48 * (60 * 60)) # 48 hour
		}

		for key in data_file:
			if key["label"] == label:
				raise Exception("the label already exists")

		data_file.append(obj_key)
		self.writeJson(data=data_file)
		return obj_key


	def get_key(self, label):
		data_file = self.readJson(self.data_file)
		for obj_key in data_file:
			if obj_key["label"] == label:
				return obj_key


	def get_obj_key(self, key):
		data_file = self.readJson(self.data_file)
		for obj_key in data_file:
			if obj_key["key"] == key:
				return obj_key


	def search_matches(self, query):
		data_file = self.readJson(self.data_file)
		matches = []
		for obj_key in data_file:
			if str(query) in str(obj_key["label"]):
				matches.append(obj_key)
		return matches


	def reValidateKey(self, key):
		data_file = self.readJson(self.data_file)
		for obj_key in data_file:
			if obj_key["key"] == key:
				obj_key["expiresAt"] = time.time() + (48 * (60 * 60)) # 48 hour
		self.writeJson(data=data_file)


	def del_key(self, key):
		data_file = self.readJson(self.data_file)
		for idx, obj_key in enumerate(deepcopy(data_file)):
			if obj_key["key"] == key:
				del data_file[idx]
				self.writeJson(data=data_file)
				return obj_key


	def del_key_by_label(self, label):
		data_file = self.readJson(self.data_file)
		for idx, obj_key in enumerate(deepcopy(data_file)):
			if obj_key["label"] == label:
				del data_file[idx]
				self.writeJson(data=data_file)
				return obj_key


	def is_valid_key(self, key):
		data_file = self.readJson(self.data_file)
		for obj_key in data_file:
			if obj_key["key"] == key:
				return True
		return False