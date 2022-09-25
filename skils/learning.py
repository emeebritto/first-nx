import nltk
import torch
import numpy as np
import torch.nn as nn
from collections import deque
from torch.utils.data import DataLoader
from utils.nltk_utils import bag_of_words, tokenords, stem
from utils.datasets import ChatDataset


nltk.download('punkt', quiet=True)
nltk.download('wordnet', quiet=True)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')


class Learning:
	def __init__(self):
		super(Learning, self).__init__()


	def bag_of_tokenords(self, sentence):
		tokenized_sentence = tokenords(sentence)
		X = bag_of_words(tokenized_sentence, self.all_words)
		X = X.reshape(1, X.shape[0])
		X = torch.from_numpy(X).to(device)
		return X


	def prepareData(self, data):
		xy = []
		for intent in data['intents']:
			tag = intent['tag']
			self.tags.append(tag)
			w = tokenords(intent['pattern'])
			self.all_words.extend(w)
			xy.append((w, tag))

		self.all_words = [stem(w) for w in self.all_words if w not in self.ignore_words]
		self.all_words = sorted(set(self.all_words))
		self.tags = sorted(set(self.tags))

		return self.splitTrainingData(xy)


	def splitTrainingData(self, xy):
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
		intents = self._loadIntents()
		X_train, y_train = self.prepareData(data=self.intents)

		self.input_size = len(X_train[0])
		self.output_size = len(self.tags)

		self._loadModel()
		self._model.train()

		dataset = ChatDataset(X_train, y_train)
		train_loader = DataLoader(
		  dataset=dataset,
		  batch_size=self.batch_size,
		  shuffle=True,
		  num_workers=0
		)

		criterion = nn.CrossEntropyLoss()
		optimizer = torch.optim.Adam(self._model.parameters(), lr=self.learning_rate)
		losses = deque([], maxlen=15)

		for epoch in range(self.num_epochs):
			for (words, labels) in train_loader:
				words = words.to(device)
				labels = labels.to(dtype=torch.long).to(device)

				outputs = self._model(words)
				loss = criterion(outputs, labels)
				optimizer.zero_grad()
				loss.backward()
				optimizer.step()

			if (epoch + 1) % 100 == 0:
				epochLoss = "%.4f" % loss.item()
				losses.append(epochLoss)
				print(f'Epoch [{epoch+1}/{self.num_epochs}], Loss: {epochLoss}')
				if losses.count(epochLoss) == 16: break

		print(f'final loss: {loss.item():.4f}')
		self._model.eval()
		self._saveMind()
