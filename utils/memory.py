from utils.functions import interval
from threading import Thread
from copy import deepcopy
from uuid import uuid4
import requests
import base64
import json
import time
import re
import os



class Memory:
	def __init__(self):
		super(Memory, self).__init__()
		self.dt_file_path = "data_register.json"
		self._cloud_url = "https://emee-nx-storage.hf.space"
		self._cache = {}
		if not os.path.exists(self.dt_file_path): self.writeRegister({})
		else: self.checkMediaFiles()


	def formatPath(self, path, rename=False, ext=""):
	  new_path = re.sub(r'\s+|\s', '-', path)
	  new_path = re.sub(r'\!|\?|\#|\*|Ç|ç|ê|Ê|ã|Ã', '', new_path)
	  if ext: new_path = self.renameExt(new_path, ext)
	  if rename: self.rename(path, new_path)
	  return new_path


	def renameExt(self, path, new_ext):
		return re.sub(r'\.\w*$', f".{new_ext}", path)


	def rename(self, path, new_path):
		os.rename(path, new_path)


	def removeFile(self, path):
		os.remove(path)


	def readJson(self, path):
		with open(path, 'r') as json_data:
			return json.load(json_data)


	def writeJson(self, path, data):
		data_file = open(path, "w")
		json.dump(data, data_file, indent=2)
		data_file.close()


	def writeRegister(self, data):
		return self.writeJson(self.dt_file_path, data)


	def start(self, gap=5):
		interval(self.checkMediaFiles, gap * 60)
		interval(self.checkCachedData, gap * 60)


	def checkMediaFiles(self):
		data_file = self.readJson(self.dt_file_path)
		for idx, file_infor in enumerate(deepcopy(data_file)):
			if file_infor["expiresAt"] < time.time():
				try:
					os.remove(file_infor["path"])
				except Exception as e:
					print(e)
				del data_file[idx]
		self.writeRegister(data=data_file)


	def checkCachedData(self):
		for key, val in self._cache.items():
			if val["expiresAt"] < time.time():
				callback = val.get("callback")
				if callback: callback(key, val)
				del self._cache[key]


	def reValidateMedia(self, path, expiresAt=60):
		formatted_path = self.formatPath(path, rename=True)
		data_file = self.readJson(self.dt_file_path)
		for file_infor in data_file:
			if file_infor["path"] == formatted_path:
				file_infor["expiresAt"] = time.time() + (expiresAt * 60)
		self.writeRegister(data=data_file)


	def reValidateCache(self, key, expiresAt=60):
		cachedData = self._cache.get(key)
		if not cachedData: return
		cachedData["expiresAt"] = time.time() + (expiresAt * 60)


	def putPath(self, path, expiresAt=60):
		formatted_path = self.formatPath(path, rename=True)
		data_file = self.readJson(self.dt_file_path)
		fc = lambda file_infor: file_infor["path"] != formatted_path
		data_file = list(filter(fc, data_file))
		new_file_infor = {
			"path": formatted_path,
			"filename": formatted_path.split("/")[-1],
			"id": str(uuid4()),
			"expiresAt": time.time() + (expiresAt * 60) # + 60 minutes
		}
		data_file.append(new_file_infor)
		self.writeRegister(data=data_file)
		return new_file_infor


	def putCache(self, key, value, expiresAt=60, callback=None):
		self._cache[key] = {
			"value": value,
			"expiresAt": time.time() + (expiresAt * 60),
			"callback": callback
		}


	def putMedia(self, filename, data, expiresAt=60):
		file_path = f"files/{filename}"
		with open(file_path, "wb") as file:
			file.write(data)
		return self.putPath(file_path, expiresAt=expiresAt)


	def delCache(self, key):
		del cache[key]


	def getCache(self, key):
		return self._cache.get(key)


	def hasFile(self, path, ext=""):
		formatted_path = self.formatPath(path, ext=ext)
		data_file = self.readJson(self.dt_file_path)
		for idx, file_infor in enumerate(deepcopy(data_file)):
			if file_infor["path"] == formatted_path:
				isFile = os.path.isfile(formatted_path)
				if not isFile:
					del data_file[idx]
					return False
				self.reValidateMedia(formatted_path)
				return True


	def getFileObjByPath(self, path):
		path = self.formatPath(path)
		data_file = self.readJson(self.dt_file_path)
		for file_infor in data_file:
			if file_infor["path"] == path:
				self.reValidate(path)
				return file_infor


	def getFileObjById(self, uid):
		data_file = self.readJson(self.dt_file_path)
		for file_infor in data_file:
			if file_infor["id"] == uid:
				self.reValidate(file_infor["path"])
				return file_infor


	def readFileById(self, uid):
		file_infor = self.getFileObjById(uid)
		if not file_infor: return
		with open(file_infor.get("path"), "rb") as file:
			file_data = file.read()
		return file_data


	def getFileUrlById(self, uid):
		file_infor = self.getFileObjById(uid)
		if not file_infor: return
		return self.getFileUrlByPath(file_infor.get("path"))


	def getFileUrlByPath(self, path):
		return f"{self._cloud_url}/file=./{path}"


	def getHttpUrl(self, filepath, mime_type="video/mp4"):
		file_size = os.path.getsize(filepath)
		CACHE_KEY = f"file::url::{filepath}::{file_size}::{mime_type}"
		cachedData = self.getCache(CACHE_KEY)
		if cachedData: return cachedData["value"]
		filename = filepath.split("/")[-1]
		with open(filepath, "rb") as rfile:
		  base = base64.b64encode(rfile.read()).decode('utf-8')
		result = requests.post(f"{self._cloud_url}/run/predict", data=json.dumps({
			"fn_index":0,
			"data":[{
				"name": filename,
				"size": file_size,
				"data": f"data:{mime_type};base64," + base 
			}],
			"session_hash":"llpx1hcnmi"
		}), headers={ "Content-Type": "application/json" })

		data = result.json()
		url = data["data"][0]
		if url: self.putCache(CACHE_KEY, url, (59 * 60)) # 59 minutes
		return url
