from utils.nltk_utils import bag_of_words, tokenords, removeVars, stem
from torch.utils.data import DataLoader
from utils.datasets import ChatDataset
from utils.functions import hashl
from collections import deque
import torch.nn as nn
import numpy as np
import torch
import tqdm
import json
import nltk
import re


nltk.download('punkt', quiet=True)
nltk.download('wordnet', quiet=True)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')


class Learning:
	def __init__(self):
		super(Learning, self).__init__()
		self.all_words = []
		self.tags = []
		self.ignore_words = []


	def _loadModel(self):
		self._model = self.neuralNet(
			self.input_size,
			self.hidden_size,
			self.output_size
		).to(device)


	def _loadData(self):
		data = torch.load(self.dataPath)
		if self.intentsHash != data["intents_hash"] or data["bag_type"] != self.bag_of_words_type:
			raise Exception

		self.input_size = data["input_size"]
		self.hidden_size = data["hidden_size"]
		self.output_size = data["output_size"]
		self.all_words = data['all_words']
		self.word_to_ix = data["word_to_ix"]
		self.ix_to_word = data["ix_to_word"]
		self.tags = data['tags']
		self.model_state = data["model_state"]


	def _loadMind(self):
		self._loadData()
		self._loadModel()

		self._model.load_state_dict(self.model_state)
		self._model.eval()


	def _loadIntents(self):
		isList = isinstance(self.intentsPath, list)
		intentsPath = self.intentsPath if isList else [self.intentsPath]
		self.intentsHash = ""
		self.intents = []
		for path in intentsPath:
			self.intentsHash += hashl(path)
			with open(path, 'r') as json_file:
				self.intents.extend(json.load(json_file))


	def bag_of_tokenords(self, sentence, method="index", tropic_words=None):
		tokenized_sentence = tokenords(sentence)
		X = bag_of_words(
			tokenized_sentence,
			self.all_words,
			method,
			tropic_words
		)
		X = X.reshape(1, X.shape[0])
		X = torch.from_numpy(X).to(device)
		return X


	def organizeIOSeq(self, data):
		def join(val, iOut):
			words = tokenords(val)
			self.all_words.extend(words)
			return (words, iOut)

		io_bag = []
		for intent in data:
			iOut = intent[self.output_name]
			self.tags.extend(iOut if isinstance(iOut, list) else [iOut])

			iInput = intent[self.input_name]
			if isinstance(iInput, list):
				for idx, val in enumerate(iInput):
					target_out = iOut[idx] if isinstance(iOut, list) else iOut
					io_bag.append(join(val, target_out))
			else:
				io_bag.append(join(iInput, iOut))

		self.all_words = [stem(w) for w in self.all_words if w not in self.ignore_words]
		self.all_words = sorted(set(self.all_words))
		self.word_to_ix = { w:idx for idx, w in enumerate(self.all_words) }
		self.ix_to_word = { idx:w for idx, w in enumerate(self.all_words) }
		try: self.tags = sorted(set(self.tags))
		except: pass

		print("bag_of_words (length): ", len(self.all_words))
		return io_bag


	def splitTrainingData(self, xy):
		X_train = []
		y_train = []
		for (pattern_sentence, tag) in xy:
		  bag = bag_of_words(
		  	pattern_sentence,
		  	self.all_words,
		  	self.bag_of_words_type
		  )
		  X_train.append(bag)
		  label = self.tags.index(tag)
		  y_train.append(label)

		X_train = np.array(X_train)
		y_train = np.array(y_train)
		return X_train, y_train


	def train(self):
		intents = self._loadIntents()
		io_bag = self.organizeIOSeq(data=self.intents)
		X_train, y_train = self.splitTrainingData(io_bag)

		self.input_size = len(X_train[0])
		self.output_size = len(self.tags)

		self._loadModel()
		self._model.train()

		dataset = ChatDataset(X_train, y_train)
		train_loader = DataLoader(
		  dataset=dataset,
		  batch_size=self.batch_size,
		  shuffle=True,
		  num_workers=2
		)

		criterion = nn.CrossEntropyLoss()
		optimizer = torch.optim.Adam(
			self._model.parameters(),
			lr=self.learning_rate
		)
		losses = deque([], maxlen=15)

		for epoch in tqdm.tqdm(range(self.num_epochs), mininterval=10., desc='training'):
			for (words, labels) in train_loader:
				words = words.to(device)
				labels = labels.to(dtype=torch.long).to(device)

				outputs = self._model(words)
				loss = criterion(outputs, labels)
				optimizer.zero_grad()
				loss.backward()
				optimizer.step()

			if (epoch + 1) % 200 == 0:
				epochLoss = "%.4f" % loss.item()
				losses.append(epochLoss)
				print(f'Epoch [{epoch+1}/{self.num_epochs}], Loss: {epochLoss}', flush=True)
				if losses.count(epochLoss) == 16: break

		print(f'final loss: {loss.item():.4f}')
		self._model.eval()
		self._saveMind()


	def probability(self, output, predicted):
		tag = self.tags[predicted.item()]
		probs = torch.softmax(output, dim=1)
		prob = probs[0][predicted.item()]
		return tag, prob.item()


	def _saveMind(self):
		data = {
			"intents_hash": self.intentsHash,
		  "model_state": self._model.state_dict(),
		  "input_size": self.input_size,
		  "hidden_size": self.hidden_size,
		  "output_size": self.output_size,
		  "all_words": self.all_words,
			"word_to_ix": self.word_to_ix,
			"ix_to_word": self.ix_to_word,
		  "bag_type": self.bag_of_words_type,
		  "tags": self.tags
		}

		if not self.dataPath:
			self.dataPath = re.sub(r'\.[a-z]*$', '.pth', self.intentsPath)

		torch.save(data, self.dataPath)
		print(f'training complete. file saved to {self.dataPath}')
