from uuid import uuid4
from random import randint, choice


class Neuron:
	def __init__(self, value):
		super(Neuron, self).__init__()
		self._id = str(uuid4())
		self._weight = randint(1, 999999999)
		self._value = value
		self._outputs = [ None ]


	def propagate(self):
		picked = choice(self._outputs)
		return picked


	def connect(self, neuralNet):
		otherNeuron = randint(0, neuralNet.length)
		self._outputs.append(otherNeuron)


	def desconnect(self, neuron):
		pass



class NeuralNet:
	def __init__(self):
		super(NeuralNet, self).__init__()
		self._neuronList = []


	@property
	def length(self):
		return len(self._neuronList)


	def learn(self, value):
		neuron = Neuron(value=value)
		self._neuronList.append(neuron)


	def predict(self, value):
		if value not in self._neuronList:
			self.learn(value)
		else:
			idx = self._neuronList.index(value)
			neuron = self._neuronList[idx]
			return neuron.propagate()


	def reStructure(self, base, output):
		idx = self._neuronList.index(base)
		neuron = self._neuronList[idx]
		neuron.desconnect(output)



neuralNet = NeuralNet()

while True:
	uInput = input("YOU: ")
	predicted = neuralNet.predict(uInput)
	print(f"Nexa (Experimental): {predicted}")
	val = input("val: ")
	if "rlearn" in val: neuralNet.reStructure(base=uInput, output=predicted)