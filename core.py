import string
import nltk
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from compiler import Compiler
from patterns.replacer import replacer
from random import choice
from mind import Mind

compiler = Compiler()



class Nexa:
	def __init__(self):
		super(Nexa, self).__init__()
		self._context_network = []
		self.name = "Nexa"
		self.age = 20
		self._actions = {}
		self.pending = {}
		self.intentsPath = "data/intents.json"
		self.dataPath = "data/data.pth"
		self.mind = Mind(intentsPath=self.intentsPath, dataPath=self.dataPath)


	@property
	def actions(self):
		return self._actions


	def read(self, value, sender="unknown"):
		if not value: return [{"msgType": "text", "msg": "..."}]
		predicted = self.mind.predict(value)
		if not predicted: return [{ "msgType": "text", "msg": "??" }]
		svars = compiler.findVars(predicted["pattern"], value)
		pendingVars = self.pending[sender]
		svars[pendingVars["name"]] = pendingVars["value"]
		print("svars", svars)
		action = predicted.get("execute")
		if action: return self.execute(action, svars)
		return [{"msgType": "text", "msg": "no actions.."}]


	def view(self, value, instruction=None, sender="unknown"):
		if not value: return
		response = []

		if instruction:
			predicted = self.mind.predict(instruction)
			if not predicted: response.insert(0, {
				"msgType": "text",
				"msg": "??"
			})
			svars = compiler.findVars(predicted["pattern"], value)
			svars["IMAGE"] = value
			action = predicted.get("execute")
			if action: return self.execute(action, svars)
		else:
			response.insert(0, {
				"msgType": "text",
				"msg": "what do I do with it?"
			})

		self.pending[sender] = {
			"name": "IMAGE",
			"value": value
		}
		return response


	def learnModule(self, module):
		for name, val in module.__dict__.items():
			if callable(val): self.learn(label=name, action=val)


	def learn(self, label, action):
		print(f"{self.name} learned to {label}")
		self._actions[label] = action


	def execute(self, label, svars):
		action = self._actions.get(label)
		if action: return action(svars, self)


	def _extractFromText(self, value, source):
		sent_tokens = nltk.sent_tokenize(source)
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
