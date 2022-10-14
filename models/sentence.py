import torch
from models.core import NeuralNet
from skils.learning import Learning



class SentenceType(Learning):
	def __init__(self):
		super(SentenceType, self).__init__()
		self.all_words = []
		self.tags = []
		self.ignore_words = [',', '!', '||']

		#files data paths
		self.dataPath = "data/sentenceType.pth"
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
		self.output_name = "type"
		self.bag_of_words_type = "index"

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
		print("prob item", prob)
		
		if prob > 0.50:
			for intent in self.intents:
				if tag == intent["type"]:
					return intent
