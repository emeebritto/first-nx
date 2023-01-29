class Message:
	def __init__(self, mType, text, sender=None):
		super(Message, self).__init__()
		self.text = text
		self.type = mType
		self.sender = sender



class Event:
	def __init__(self):
		super(Event, self).__init__()
		self._notify = lambda msgType, msg: print("Event -> no function was defined yet")


	def onMessage(self, func):
		self._notify = func


	def newMessage(self, msg):
		self._notify(msg)


	def wait_reply(self, msg):
		return self._notify(msg)