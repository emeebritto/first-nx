import nltk
import json
import torch
import string
import numpy as np
import torch.nn as nn
from collections import deque
from torch.utils.data import DataLoader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from utils.nltk_utils import bag_of_words, tokenize, stem
from utils.functions import some_match, hashl
from utils.datasets import ChatDataset
from models.core import NeuralNet


nltk.download('punkt', quiet=True)
nltk.download('wordnet', quiet=True)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')


class NexaMind:
	def __init__(self, intentsPath, dataPath):
		super(NexaMind, self).__init__()
		self.all_words = []
		self.tags = []
		self.ignore_words = ['?', '.', '!', ',', '||']

		self.dataPath = dataPath
		self.intentsPath = intentsPath
		self.intentsHash = None

		# Hyper-parameters 
		self.num_epochs = 5000
		self.batch_size = 100
		self.learning_rate = 0.001
		self.input_size = None
		self.hidden_size = 8
		self.output_size = None

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
		output = self._model(value)
		_, predicted = torch.max(output, dim=1)

		print(self.tags)

		print(predicted)
		print(predicted.item())

		tag = self.tags[predicted.item()]
		probs = torch.softmax(output, dim=1)
		prob = probs[0][predicted.item()]
		
		if prob.item() > 0.75:
			for intent in self.intents['intents']:
				if tag == intent["tag"]:
					return intent["tag"]


	def _createTrainingData(self, xy):
		X_train = []
		y_train = []
		for (pattern_sentence, tag) in xy:
		  bag = bag_of_words(pattern_sentence, self.all_words)
		  X_train.append(bag)
		  label = self.tags.index(tag)
		  y_train.append(label)

		X_train = np.array(X_train)
		y_train = np.array(y_train)
		return X_train, y_train


	def train(self):
		xy = []
		self._loadIntents()
		for intent in self.intents['intents']:
		  tag = intent['tag']
		  self.tags.append(tag)
		  for pattern in intent['patterns']:
		    w = tokenize(pattern)
		    self.all_words.extend(w)
		    xy.append((w, tag))

		self.all_words = [stem(w) for w in self.all_words if w not in self.ignore_words]
		self.all_words = sorted(set(self.all_words))
		self.tags = sorted(set(self.tags))

		X_train, y_train = self._createTrainingData(xy)
		self.input_size = len(X_train[0])
		self.output_size = len(self.tags)

		self._loadModel()

		dataset = ChatDataset(X_train, y_train)
		train_loader = DataLoader(
		  dataset=dataset,
		  batch_size=self.batch_size,
		  shuffle=True,
		  num_workers=0
		)

		criterion = nn.CrossEntropyLoss()
		optimizer = torch.optim.Adam(self._model.parameters(), lr=self.learning_rate)
		losses = deque([], maxlen=7)

		for epoch in range(self.num_epochs):
			for (words, labels) in train_loader:
				words = words.to(device)
				labels = labels.to(dtype=torch.long).to(device)

				outputs = self._model(words)
				loss = criterion(outputs, labels)
				optimizer.zero_grad()
				loss.backward()
				optimizer.step()

			if (epoch+1) % 100 == 0:
				epochLoss = "%.4f" % loss.item()
				losses.append(epochLoss)
				print(f'Epoch [{epoch+1}/{self.num_epochs}], Loss: {epochLoss}')
				if losses.count(epochLoss) == 6: break

		print(f'final loss: {loss.item():.4f}')
		self._saveMind()


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