import nltk
import random
import json
import torch
import string
import numpy as np
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from utils.nltk_utils import bag_of_words, tokenize, stem
from utils.functions import some_match, hashl


nltk.download('punkt', quiet=True)
nltk.download('wordnet', quiet=True)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')



class ChatDataset(Dataset):

  def __init__(self, X_train, y_train):
    self.n_samples = len(X_train)
    self.x_data = X_train
    self.y_data = y_train

  def __getitem__(self, index):
    return self.x_data[index], self.y_data[index]


  def __len__(self):
    return self.n_samples



class NeuralNet(nn.Module):
  def __init__(self, input_size, hidden_size, num_classes):
    super(NeuralNet, self).__init__()
    self.l1 = nn.Linear(input_size, hidden_size) 
    self.l2 = nn.Linear(hidden_size, hidden_size) 
    self.l3 = nn.Linear(hidden_size, num_classes)
    self.relu = nn.ReLU()
  
  def forward(self, x):
    out = self.l1(x)
    out = self.relu(out)
    out = self.l2(out)
    out = self.relu(out)
    out = self.l3(out)
    # no activation and no softmax at the end
    return out



class Nexa:
	def __init__(self):
		super(Nexa, self).__init__()
		self.name = "Nexa"
		self.context_network = []
		self.all_words = []
		self.tags = []
		self.ignore_words = ['?', '.', '!', ',', '||']

		self.mindPath = "data/data.pth"
		self.intentsPath = "data/intents.json"
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


	def _translate(self, value):
		tokenized_value = tokenize(value)
		X = bag_of_words(tokenized_value, self.all_words)
		X = X.reshape(1, X.shape[0])
		X = torch.from_numpy(X).to(device)
		return X


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
		data = torch.load(self.mindPath)
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


	def read(self, value):
		if not value: return ""

		valueTranslated = self._translate(value)

		output = self._model(valueTranslated)
		_, predicted = torch.max(output, dim=1)

		tag = self.tags[predicted.item()]
		probs = torch.softmax(output, dim=1)
		prob = probs[0][predicted.item()]

		if prob.item() > 0.75:
		  for intent in self.intents['intents']:
		    hasContext = some_match(self.context_network, intent["context"]) if intent["context"] else True
		    if tag == intent["tag"] and hasContext:
		      self.context_network.append(intent["tag"])
		      response = random.choice(intent['responses'])
		      return response
		    elif tag == intent["tag"]:
		      return "??"
		else:
			with open('data/about_me.md', 'r') as f:
			  nexaMd = f.read()

			sent_tokens = nltk.sent_tokenize(nexaMd)
			remove_punct_dict = dict((ord(punct),None) for punct in string.punctuation)

			def LemNormalize(text):
			  return nltk.word_tokenize(text.lower().translate(remove_punct_dict))

			value = value.lower()
			nexa_response = ""
			sent_tokens.append(value)
			tfidfvec = TfidfVectorizer(tokenizer=LemNormalize , stop_words='english')
			tfidf = tfidfvec.fit_transform(sent_tokens)
			val = cosine_similarity(tfidf[-1], tfidf)
			idx = val.argsort()[0][-2]
			flat = val.flatten()
			flat.sort()
			score = flat[-2]
			if score == 0: nexa_response = "sorry, I dont understand"
			else: nexa_response = sent_tokens[idx]

			sent_tokens.remove(value)
			return nexa_response


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
		    print (f'Epoch [{epoch+1}/{self.num_epochs}], Loss: {loss.item():.4f}')

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

		torch.save(data, self.mindPath)
		print(f'training complete. file saved to {self.mindPath}')
