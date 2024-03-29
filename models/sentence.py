import torch
from models.core import NeuralNet
from skils.learning import Learning



class Sentence(Learning):
	def __init__(self, out, bag_type="index"):
		super(Sentence, self).__init__()
		self.all_words = []
		self.tags = []
		self.ignore_words = [',', '!', '||']

		#files data paths
		self.dataPath = f"data/sentence_{out}.pth"
		self.intentsPath = ["data/sentence.json", "data/intents.json"]
		self.intentsHash = ""

		# Hyper-parameters 
		self.neuralNet = NeuralNet
		self.num_epochs = 400
		self.batch_size = 100
		self.learning_rate = 0.001
		self.input_size = None # it will be defined in runtime
		self.hidden_size = 40
		self.output_size = None # it will be defined in runtime

		self.input_name = "pattern"
		self.output_name = out
		self.bag_of_words_type = bag_type

		self._model = None
		self._loadIntents()

		try:
			self._loadMind()
		except Exception as e:
			self.train()


	def predict(self, value):
		X = self.bag_of_tokenords(value, self.bag_of_words_type)

		output = self._model(X)
		_, predicted = torch.max(output, dim=1)
		tag, prob = self.probability(output, predicted)
		
		if prob > 0.50:
			for intent in self.intents:
				if tag == intent[self.output_name]:
					return intent
