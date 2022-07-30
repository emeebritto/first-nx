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
	def __init__(self):
		super(NexaMind, self).__init__()
		self.all_words = []
		self.ignore_words = ['.', ',', '||']

		self.dataPath = "data/data.pth"
		self.intentsPath = "data/intents.json"
		self.intentsHash = None

		# Hyper-parameters
		self.epoch = 0 
		self.num_epochs = 5000
		self.batch_size = 100
		self.learning_rate = 0.001
		self.input_size = None
		self.hidden_size = 8
		self.output_size = None

		self._model = None

		try:
			self._loadMind()
		except Exception as e:
			print("no data detected, it will be created soon")


	def _format(self, value):
		tokenized_value = tokenize(value)
		self.all_words.extend(tokenized_value)
		self.all_words = [stem(w) for w in self.all_words if w not in self.ignore_words]
		self.all_words = sorted(set(self.all_words))
		X = bag_of_words(tokenized_value, self.all_words)
		return X


	def _loadModel(self):
		self._model = NeuralNet(
			self.input_size,
			self.hidden_size,
			self.output_size
		).to(device)


	def _loadMind(self):
		data = torch.load(self.dataPath)

		self.epoch = data["epoch"]
		self.input_size = data["input_size"]
		self.hidden_size = data["hidden_size"]
		self.output_size = data["output_size"]
		self.all_words = data['all_words']
		self.model_state = data["model_state"]

		self._loadModel()

		self._model.load_state_dict(self.model_state)
		self._model.eval()


	def predict(self, value):
		valueFormated = self._format(value)
		self.input_size = len(valueFormated)
		valueFormated = valueFormated.reshape(1, valueFormated.shape[0])
		valueFormated = torch.from_numpy(valueFormated).to(device)
		self.output_size = len(self.all_words) + 1

		self._loadModel()
		criterion = nn.CrossEntropyLoss()
		optimizer = torch.optim.Adam(self._model.parameters(), lr=self.learning_rate)

		self.epoch += 1

		tokenized_value = tokenize(input("expected: "))
		expected = bag_of_words(tokenized_value, self.all_words)

		dataset = ChatDataset(valueFormated, expected)
		train_loader = DataLoader(dataset=dataset, batch_size=self.batch_size)

		for (words, labels) in train_loader:
			words = words.to(device)
			labels = labels.to(dtype=torch.long).to(device)

			outputs = self._model(words)
			print(labels.shape)
			print(labels)
			loss = criterion(outputs, labels)
			optimizer.zero_grad()
			loss.backward()
			optimizer.step()

			print(f'Epoch [{self.epoch}/{self.num_epochs}], Loss: {"%.4f" % loss.item()}')
			self._saveMind()

			print(self.all_words)

			response = []

			for idx, out in enumerate(outputs[0]):
				print(self.all_words[idx - 1], out)
				if out > 0.2:
					response.append(self.all_words[idx - 1])

			return response


		# _, predicted = torch.max(outputs, dim=1)
		# tag = self.tags[predicted.item()]
		# probs = torch.softmax(outputs, dim=1)
		# prob = probs[0][predicted.item()]
		
		# if prob.item() > 0.75:
		# 	for intent in self.intents:
		# 		if tag == intent["tag"]:
		# 			return intent["tag"]


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
		for intent in self.intents:
			tag = intent['tag']
			self.tags.append(tag)
			w = tokenize(intent['pattern'])
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
		  "model_state": self._model.state_dict(),
		  "epoch": self.epoch,
		  "input_size": self.input_size,
		  "hidden_size": self.hidden_size,
		  "output_size": self.output_size,
		  "all_words": self.all_words
		}

		torch.save(data, self.dataPath)
		print(f'checkpoint was saved to {self.dataPath}')
