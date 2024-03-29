from utils.functions import read_as_binary, create_filePath, raiseError
from api.flask import memory
from random import choice
import hashlib
import base64
import imghdr
import magic



class File:
	def __init__(self, value, mime_type=None):
		super(File, self).__init__()
		self.isbuffer = isinstance(value, bytes)
		self.isUrl = not self.isbuffer and "http" in value[:5]
		self.value = value
		self.mime_type = mime_type or self._getMimeType()
		self.ext = self._getFileExt()
		self.mime_type = self._fixMime()


	def __repr__(self):
		return self.path


	def __str__(self):
		return self.path


	def _getMimeType(self):
		# mime = magic.Magic(mime=True)
		if self.isUrl: return "link/url"
		if self.isbuffer: return magic.from_buffer(self.value)
		return magic.from_file(self.value, mime=True)


	def _fixMime(self):
		if "image" in self.mime_type: return f"image/{self.ext}"
		return self.mime_type


	def _getFileExt(self):
		if isinstance(self.value, bytes):
			return imghdr.what(None, self.value)
		return self.mime_type.split("/")[1]


	def _getDataFromUrl(self):
		pass


	def _b64encode(self, value):
		base = base64.b64encode(value).decode('utf-8')
		return f"data:{self.mime_type};base64," + base


	def read_as(self, stype):
		types = {
			"url": self.as_url,
			"bin": self.as_binary,
			"base64": self.as_base64
		}

		return types.get(stype, self.as_binary)()


	def as_binary(self):
		if self.isbuffer or self.isUrl: return self.value
		return read_as_binary(self.value)


	def as_url(self):
		if self.isUrl: return self.value
		if not self.isbuffer: return memory.getHttpUrl(self.value, mime_type=self.mime_type)
		file_hash = hashlib.sha256()
		file_hash.update(self.value)
		file_hash = file_hash.hexdigest()
		filePath = create_filePath(self.value, fileName=file_hash, fileFormat=self.ext)
		file_url = memory.getHttpUrl(filePath, mime_type=self.mime_type)
		memory.removeFile(filePath)
		return file_url


	def as_base64(self):
		if self.isUrl: return self.value
		if self.isbuffer: return self._b64encode(self.value)
		with open(self.value, "rb") as rfile:
			return self._b64encode(rfile.read())



class NxConfig:
	def __init__(self, **kwargs):
		super(NxConfig, self).__init__()
		self.file_as = kwargs.get("file_as", "bin")
		raiseError(
			msg='invalid file type (file_as)',
			case=self.file_as not in ["url", "bin", "base64"]
		)



class Response:
	def __init__(self, target, asyncResponse=None, config=None):
		super(Response, self).__init__()
		self.target = target
		self._config = config or NxConfig()
		self._sequence = []
		self._main = []
		self._asyncRes = asyncResponse or {}


	def __repr__(self):
		return self._sequence


	def __len__(self):
		return len(self._sequence)


	@property
	def sequence(self):
		return self._sequence


	def last_from_seq(self):
		return self._sequence[-1]


	def _instantMsg(self, value):
		reply_method = self._asyncRes.get(value["msgType"])
		if reply_method: reply_method(value["msg"])
		if self.target: self.emit("new_nx_message", value, room=self.target)


	def _append(self, value):
		self._sequence.append(value)
		self._instantMsg(value)
		return self;


	def emit(self, *args, **kwargs):
		io = self._asyncRes.get("socket")
		if io: io.emit(*args, **kwargs)


	def sendText(self, value):
		self._instantMsg({"msgType": "text", "msg": value})
		return self;


	def appendText(self, value, choiceOne=False):
		if isinstance(value, str):
			self._append({"msgType": "text", "msg": value})
		elif isinstance(value, list):
			if choiceOne:
				self._append({"msgType": "text", "msg": choice(value)})
			else:
				for text in value:
					self._append({"msgType": "text", "msg": text})
		else:
			raise Exception("appendText method has not received a str either list value")
		return self


	def appendDocument(self, value, mime_type=None):
		file = File(value, mime_type)
		return self._append({
			"msgType": "document",
			"msg": file.read_as(self._config.file_as)
		})


	def appendVideo(self, value, mime_type=None):
		file = File(value, mime_type)
		return self._append({
			"msgType": "video",
			"msg": file.read_as(self._config.file_as)
		})


	def appendPhoto(self, value, mime_type=None):
		file = File(value, mime_type)
		return self._append({
			"msgType": "photo",
			"msg": file.read_as(self._config.file_as)
		})


	def appendAnimation(self, value):
		self._append({"msgType": "animation", "msg": value})
		return self


	def appendAudio(self, value):
		self._append({"msgType": "audio", "msg": value})
		return self