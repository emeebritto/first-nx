from uuid import uuid4
from random import randint, choice


class Neuron:
	def __init__(self, value):
		super(Neuron, self).__init__()
		self._id = str(uuid4())
		self._weight = randint(1, 999999999)
		self._activationKeys = []
		self._value = value
		self._inputs = [ None ]
		self._outputs = [ None ]


	def __str__(self):
		return self._value


	def __repr__(self):
		return self._value


	@property
	def weight(self):
		return self._weight


	@property
	def value(self):
		return self._value


	def propagate(self):
		picked = choice(self._outputs)
		return picked


	def propagateByVal(self, values, weight=0):
		value = value[1:]
		for output in self._outputs:
			if output.value == value[0]:
				output.propagateByVal(value, self._weight + weight)


	def setActivationKey(self, key):
		self._activationKeys.append(key)


	def setInput(self, neuron):
		self._inputs.append(neuron)


	def connect(self, otherNeuron, weight=None):
		self._outputs.append(otherNeuron)
		otherNeuron.setInput(self)
		otherNeuron.setActivationKey(weight or self.weight)


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
		return neuron


	def findByVal(self, value):
		for neuron in self._neuronList:
			if neuron.value == value:
				return neuron


	def predict(self, value):
		value = value.split()
		globalWeight = 0
		lastNeuron = None
		for idx, word in enumerate(value):
			neuron = self.findByVal(word)
			if not neuron:
				lastNeuron = self.learn(word)
			else:
				if lastNeuron and not neuron.hasInput(lastNeuron):
					lastNeuron.connect(neuron, weight=globalWeight)
					lastNeuron = neuron
			globalWeight += lastNeuron.weight
		neuron = findByVal(value[0])
		neuron.propagateByVal(value)


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