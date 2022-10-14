import string
import nltk
import numpy as np
from models.transformers import answer_by_context
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from compiler import Compiler
from patterns.replacer import replacer
from random import choice
from analyzer import Analyzer
from mind import Mind

compiler = Compiler()



class Response:
	def __init__(self):
		super(Response, self).__init__()
		self._response = []


	def __repr__(self):
		return self._response


	def __len__(self):
		return len(self._response)


	def values(self):
		return self._response


	def appendText(self, msg, choiceOne=False):
		if isinstance(msg, str):
			self._response.append({"msgType": "text", "msg": msg})
		elif isinstance(msg, list):
			if choiceOne:
				self._response.append({"msgType": "text", "msg": choice(msg)})
			else:
				for text in msg:
					self._response.append({"msgType": "text", "msg": text})
		else:
			raise Exception("appendText method has not received a str either list value")
		return self._response


	def appendDocument(self, msg):
		self._response.append({"msgType": "document", "msg": msg})
		return self._response


	def appendVideo(self, msg):
		self._response.append({"msgType": "video", "msg": msg})
		return self._response


	def appendPhoto(self, msg):
		self._response.append({"msgType": "photo", "msg": msg})
		return self._response


	def appendAnimation(self, msg):
		self._response.append({"msgType": "animation", "msg": msg})
		return self._response


	def appendAudio(self, msg):
		self._response.append({"msgType": "audio", "msg": msg})
		return self._response




class Nexa(Mind):
	def __init__(self):
		super(Nexa, self).__init__()
		self._context_network = []
		self.name = "Nexa"
		self.me = self.about()
		self._actions = {}
		self.pending = {}
		self.analyzer = Analyzer()


	@property
	def actions(self):
		return self._actions


	def about(self):
		with open("data/about_me.md", "r") as file:
			return file.read()


	def read(self, value, context="", sender="unknown"):
		res = Response()
		if not value: return res.appendText("...")
		print(self.analyzer.type(value))

		if self.analyzer.isQuestion(value):
			answer = answer_by_context(context=self.me + context, value=value)
			if answer: return res.appendText(answer)

		if self.analyzer.isOrder(value):
			predicted = self.predict(value) #.high_precision()

			if not predicted.intent: return res.appendText("??")
			print("predicted intent", predicted.intent)
			svars = compiler.findVars(predicted.intent["pattern"], value)
			pendingVars = self.pending.get(sender)

			if pendingVars:
				svars[pendingVars["name"]] = pendingVars["value"]
				del self.pending[sender]
			print("svars", svars)
			action = predicted.intent.get("execute")

			if action: self.execute(action, svars, res)
			responses = predicted.intent.get("response")

			if responses: res.appendText(responses, choiceOne=True)
			return res.values()


	def view(self, value, instruction=None, sender="unknown"):
		if not value: return
		res = Response()

		if instruction:
			predicted = self.predict(instruction)
			if not predicted: res.appendText("??")
			svars = compiler.findVars(predicted["pattern"], value)
			svars["IMAGE"] = value
			action = predicted.get("execute")
			if action: return self.execute(action, svars, res)
		else:
			res.appendText("what do I do with it?")

		self.pending[sender] = {
			"name": "IMAGE",
			"value": value
		}

		return res.values()


	def learnModule(self, module):
		for name, val in module.__dict__.items():
			if callable(val): self.learn(label=name, action=val)


	def learn(self, label, action):
		print(f"{self.name} learned to {label}")
		self._actions[label] = action


	def execute(self, label, svars, res):
		action = self._actions.get(label)
		if action: return action(svars, self, res)


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
