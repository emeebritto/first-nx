class Inbox:
	def __init__(self):
		super(Inbox, self).__init__()
		self._notify = lambda msgType, msg: print("Inbox -> no function was defined yet")


	def onMessage(self, func):
		self._notify = func


	def newMessage(self, msgType, msg):
		self._notify(msgType, msg)


	def wait_reply(self, msgType, msg):
		return self._notify(msgType, msg)