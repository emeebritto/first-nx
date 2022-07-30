from nexa.nexaMind import NexaMind
from nexa.compiler import Compiler


class Nexa(NexaMind):
	def __init__(self):
		super(Nexa, self).__init__()
		self.context_network = []
		self.name = "Nexa"


	def read(self, value):
		if not value: return ""
		return self.predict(value)
