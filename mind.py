import json
import torch
import numpy as np
import torch.nn as nn
from utils.functions import hashl
from models.core import NeuralNet
from skils.learning import Learning


device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')


class Mind(Learning):
	def __init__(self, intentsPath, dataPath):
		super(Mind, self).__init__()
		self.all_words = []
		self.tags = []
		self.ignore_words = [',', '!', '||']

		self.dataPath = dataPath
		self.intentsPath = intentsPath
		self.intentsHash = None

		# Hyper-parameters 
		self.num_epochs = 6000
		self.batch_size = 100
		self.learning_rate = 0.001
		self.input_size = None # it will be defined in runtime
		self.hidden_size = 40
		self.output_size = None # it will be defined in runtime

		self._model = None
		self._loadIntents()

		try:
			self._loadMind()
		except Exception as e:
			self.train()


	def _loadModel(self):
		self._model = NeuralNet(
			self.input_size,
			self.hidden_size,
			self.output_size
		).to(device)


	def _loadIntents(self):
		self.intentsHash = hashl(self.intentsPath)
		with open(self.intentsPath, 'r') as json_data:
			self.intents = json.load(json_data)


	def _loadMind(self):
		data = torch.load(self.dataPath)
		if self.intentsHash != data["intents_hash"]:
			raise Exception

		self.input_size = data["input_size"]
		self.hidden_size = data["hidden_size"]
		self.output_size = data["output_size"]
		self.all_words = data['all_words']
		self.tags = data['tags']
		self.model_state = data["model_state"]

		self._loadModel()

		self._model.load_state_dict(self.model_state)
		self._model.eval()


	def predict(self, value):
		X = self.bag_of_tokenords(value)

		output = self._model(X)
		_, predicted = torch.max(output, dim=1)

		tag = self.tags[predicted.item()]
		probs = torch.softmax(output, dim=1)
		prob = probs[0][predicted.item()]
		print("prob item", prob.item())
		
		if prob.item() > 0.50:
			for intent in self.intents['intents']:
				if tag == intent["tag"]:
					return intent


	def _saveMind(self):
		data = {
			"intents_hash": self.intentsHash,
		  "model_state": self._model.state_dict(),
		  "input_size": self.input_size,
		  "hidden_size": self.hidden_size,
		  "output_size": self.output_size,
		  "all_words": self.all_words,
		  "tags": self.tags
		}

		torch.save(data, self.dataPath)
		print(f'training complete. file saved to {self.dataPath}')
